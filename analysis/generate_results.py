import os
import glob
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Pfade definieren
script_dir = os.path.dirname(os.path.abspath(__file__))

# Zielordner 'images' auf Skripthöhe
image_output_dir = os.path.join(script_dir, "images")
os.makedirs(image_output_dir, exist_ok=True)

base_measurement_dir = os.path.join(script_dir, "../messurement")

# 2. Feste Basisfarben für die RMW-Implementierungen
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

# 3. Alle Einzelwerte einlesen und summieren
all_raw_data = []

for folder_path in sorted(subfolders):
    folder_name = os.path.basename(folder_path)
    txt_files = glob.glob(os.path.join(folder_path, '*.txt'))

    for file_path in txt_files:
        file_name = os.path.basename(file_path)
        
        match = re.match(r"([a-zA-Z0-9]+)_cpp_results_(rmw_[a-zA-Z0-9_]+?)_nr_\d+\.txt", file_name)
        if not match:
            continue  
            
        sensor_type = match.group(1).upper() if match.group(1).lower() in ["imu"] else match.group(1).capitalize()
        rmw_name = match.group(2)
        
        total_nanoseconds = 0
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                entry_count = 0
                for line in file:
                    cleaned_line = line.strip()
                    if not cleaned_line:
                        continue
                    
                    entry_count += 1
                    # Erste 10 Einträge überspringen (Warm-up-Phase)
                    if entry_count <= 10:
                        continue
                    
                    number_part = cleaned_line.split()[0]
                    total_nanoseconds += int(number_part)
                    
            total_milliseconds = total_nanoseconds / 1_000_000
            
            all_raw_data.append({
                "Durchlauf (Ordner)": folder_name,
                "Sensor": sensor_type,
                "RMW Implementation": rmw_name,
                "Gesamtzeit (ms)": total_milliseconds
            })
        except Exception as e:
            print(f"Fehler beim Parsen von {file_name}: {e}")

df_raw = pd.DataFrame(all_raw_data)

if df_raw.empty:
    print("Keine auswertbaren Daten gefunden!")
    exit(0)

# 4. Daten aggregieren
df = df_raw.groupby(
    ["Sensor", "RMW Implementation", "Durchlauf (Ordner)"], 
    as_index=False
)["Gesamtzeit (ms)"].sum()

sns.set_theme(style="whitegrid")

# 5. Kombinierte Figure erstellen (1 Zeile, N Spalten)
unique_sensors = sorted(df["Sensor"].unique())
num_sensors = len(unique_sensors)

fig, axes = plt.subplots(1, num_sensors, figsize=(6.5 * num_sensors, 6.5), squeeze=False)
axes = axes.flatten()

for idx, sensor_type in enumerate(unique_sensors):
    ax = axes[idx]
    df_filtered = df[df["Sensor"] == sensor_type].copy()
    
    # RMWs nach kumulierter Gesamtdauer aufsteigend sortieren
    rmw_order = (
        df_filtered.groupby("RMW Implementation")["Gesamtzeit (ms)"]
        .sum()
        .sort_values(ascending=True)
        .index.tolist()
    )
    
    unique_runs = sorted(df_filtered["Durchlauf (Ordner)"].unique())
    num_runs = len(unique_runs)

    barplot = sns.barplot(
        data=df_filtered,
        x="RMW Implementation",
        y="Gesamtzeit (ms)",
        hue="Durchlauf (Ordner)",
        order=rmw_order,
        ax=ax
    )
    
    # Legende aus dem jeweiligen Subplot entfernen
    if ax.get_legend() is not None:
        ax.get_legend().remove()
    
    # RMW-Farben mit feiner Kontur anwenden
    for run_idx in range(num_runs):
        for rmw_idx, rmw_name in enumerate(rmw_order):
            base_col = RMW_BASE_COLORS.get(rmw_name, DEFAULT_BASE_COLOR)
            patch_idx = run_idx * len(rmw_order) + rmw_idx
            if patch_idx < len(barplot.patches):
                patch = barplot.patches[patch_idx]
                patch.set_facecolor(base_col)
                patch.set_edgecolor("#222222")
                patch.set_linewidth(0.8)

    # Subplot-Titel und Achsen
    ax.set_title(f"{sensor_type}", fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel("Middleware-Implementierung (RMW)", fontsize=10, fontweight='bold', labelpad=10)
    ax.set_ylabel("Gesamtlaufzeit [ms]", fontsize=10, fontweight='bold', labelpad=10)
    ax.tick_params(axis='x', rotation=20)
    
    # Zahlenwerte über den Balken
    for p in barplot.patches:
        height = p.get_height()
        if height > 0:
            formatted_val = f"{height:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")
            ax.annotate(
                f"{formatted_val} ms",
                (p.get_x() + p.get_width() / 2., height),
                ha='center', va='bottom',
                xytext=(0, 4), 
                textcoords='offset points', 
                fontsize=8,
                fontweight='bold',
                rotation=45
            )
            
    # Y-Achse nach oben erweitern, damit Labels nicht abgeschnitten werden
    ax.set_ylim(top=ax.get_ylim()[1] * 1.15)

# Gesamttitel für das Gesamtbild
plt.suptitle("ROS 2 Performance-Benchmark nach Sensortyp", fontsize=15, fontweight='bold', y=1.02)
plt.tight_layout()

# 6. Kombiniertes Bild speichern
output_filename = "benchmarks_all_sensors_combined.png"
save_path = os.path.join(image_output_dir, output_filename)

plt.savefig(save_path, dpi=300, bbox_inches='tight')
plt.close(fig)

print(f"\nKombiniertes Benchmark-Diagramm erfolgreich gespeichert: {save_path}")