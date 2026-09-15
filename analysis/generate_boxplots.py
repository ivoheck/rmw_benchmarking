import os
import glob
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Pfade definieren
script_dir = os.path.dirname(os.path.abspath(__file__))

image_output_dir = os.path.join(script_dir, "images")
os.makedirs(image_output_dir, exist_ok=True)

base_measurement_dir = os.path.join(script_dir, "../messurement")

# 2. Feste Farbpalette für die RMWs
RMW_BASE_COLORS = {
    "rmw_cyclonedds_cpp": "#1f77b4",    # Blau
    "rmw_fastrtps_cpp": "#ff7f0e",      # Orange
    "rmw_connextdds": "#2ca02c",        # Grün
    "rmw_zenoh_cpp": "#d62728",         # Rot
    "rmw_gurumdds_cpp": "#9467bd"       # Lila
}
DEFAULT_BASE_COLOR = "#7f7f7f"

if not os.path.exists(base_measurement_dir):
    print(f"Fehler: Das Verzeichnis '{base_measurement_dir}' existiert nicht!")
    exit(1)

subfolders = [
    os.path.join(base_measurement_dir, d) 
    for d in os.listdir(base_measurement_dir) 
    if os.path.isdir(os.path.join(base_measurement_dir, d))
]

if not subfolders:
    print(f"Keine Messordner in '{base_measurement_dir}' gefunden!")
    exit(1)

# 3. Alle Einzelwerte einlesen
all_samples = []

for folder_path in sorted(subfolders):
    txt_files = glob.glob(os.path.join(folder_path, '*.txt'))

    for file_path in txt_files:
        file_name = os.path.basename(file_path)
        
        match = re.match(r"([a-zA-Z0-9]+)_cpp_results_(rmw_[a-zA-Z0-9_]+?)_nr_\d+\.txt", file_name)
        if not match:
            continue  
            
        sensor_type = match.group(1).upper() if match.group(1).lower() in ["imu"] else match.group(1).capitalize()
        rmw_name = match.group(2)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                entry_count = 0
                for line in file:
                    cleaned_line = line.strip()
                    if not cleaned_line:
                        continue
                    
                    entry_count += 1
                    # Erste 50 Einträge (Warm-up) verwerfen
                    if entry_count <= 50:
                        continue
                    
                    number_part = cleaned_line.split()[0]
                    lat_us = int(number_part) / 1_000.0  # Nanosekunden zu Mikrosekunden
                    
                    all_samples.append({
                        "Sensor": sensor_type,
                        "RMW Implementation": rmw_name,
                        "Latenz (µs)": lat_us
                    })
        except Exception as e:
            print(f"Fehler beim Parsen von {file_name}: {e}")

df_samples = pd.DataFrame(all_samples)

if df_samples.empty:
    print("Keine auswertbaren Daten gefunden!")
    exit(0)

sns.set_theme(style="whitegrid")

# 4. Kombinierte Figure erstellen
unique_sensors = sorted(df_samples["Sensor"].unique())
num_sensors = len(unique_sensors)

# Dynamische Bildgröße: ca. 6.5 Zoll Breite pro Sensor
fig, axes = plt.subplots(1, num_sensors, figsize=(6.5 * num_sensors, 6.0), squeeze=False)
axes = axes.flatten()

for idx, sensor_type in enumerate(unique_sensors):
    ax = axes[idx]
    df_sensor = df_samples[df_samples["Sensor"] == sensor_type].copy()
    
    raw_max = df_sensor["Latenz (µs)"].max()
    
    # Ausreißer-Bereinigung je RMW
    q25 = df_sensor.groupby("RMW Implementation")["Latenz (µs)"].transform(lambda x: x.quantile(0.25))
    q75 = df_sensor.groupby("RMW Implementation")["Latenz (µs)"].transform(lambda x: x.quantile(0.75))
    cutoff = q75 + (1.5 * (q75 - q25))
    
    df_cleaned = df_sensor[df_sensor["Latenz (µs)"] <= cutoff].copy()
    
    cleaned_max = df_cleaned["Latenz (µs)"].max()
    cleaned_min = df_cleaned["Latenz (µs)"].min()
    print(f"[{sensor_type}] Bereinigung: Roh-Max: {raw_max:.1f} µs -> Neues Max: {cleaned_max:.1f} µs")

    # RMWs nach dem Median sortieren
    rmw_order = (
        df_cleaned.groupby("RMW Implementation")["Latenz (µs)"]
        .median()
        .sort_values(ascending=True)
        .index.tolist()
    )
    
    current_palette = {
        rmw: RMW_BASE_COLORS.get(rmw, DEFAULT_BASE_COLOR) 
        for rmw in rmw_order
    }
    
    # Boxplot in das jeweilige Subplot-Axes-Objekt zeichnen
    sns.boxplot(
        data=df_cleaned,
        x="RMW Implementation",
        y="Latenz (µs)",
        order=rmw_order,
        palette=current_palette,
        hue="RMW Implementation",
        legend=False,
        showmeans=True,
        showfliers=False,
        meanprops={
            "marker": "^", 
            "markerfacecolor": "white", 
            "markeredgecolor": "black", 
            "markersize": "7"
        },
        ax=ax
    )
    
    # Eigene dynamische Y-Achsenskalierung pro Sensor-Plot
    padding = (cleaned_max - cleaned_min) * 0.1
    ax.set_ylim(bottom=max(0, cleaned_min - padding), top=cleaned_max + padding)
    
    ax.set_title(f"{sensor_type}", fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel("Middleware-Implementierung (RMW)", fontsize=10, fontweight='bold', labelpad=10)
    ax.set_ylabel("Latenz [µs]", fontsize=10, fontweight='bold', labelpad=10)
    ax.tick_params(axis='x', rotation=20)

plt.suptitle("ROS 2 Latenzverteilung nach Sensortyp", fontsize=15, fontweight='bold', y=1.02)
plt.tight_layout()

# 5. Gemeinsames Bild speichern
output_filename = "boxplots_all_sensors_combined.png"
save_path = os.path.join(image_output_dir, output_filename)

plt.savefig(save_path, dpi=300, bbox_inches='tight')
plt.close(fig)

print(f"\nKombiniertes Diagramm erfolgreich gespeichert: {save_path}")