import os
import glob
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Pfade definieren
script_dir = os.path.dirname(os.path.abspath(__file__))

# Zielordner 'images' auf Höhe des Skripts
image_output_dir = os.path.join(script_dir, "images")
os.makedirs(image_output_dir, exist_ok=True)

# Basis-Pfad zu den Messungen
base_measurement_dir = os.path.join(script_dir, "../messurement")

# 2. Feste Basisfarben für die RMW-Implementierungen
RMW_BASE_COLORS = {
    "rmw_cyclonedds_cpp": "#1f77b4",    # Blau
    "rmw_fastrtps_cpp": "#ff7f0e",      # Orange
    "rmw_connextdds": "#2ca02c",        # Grün
    "rmw_zenoh_cpp": "#d62728",         # Rot
    "rmw_gurumdds_cpp": "#9467bd"       # Lila
}
DEFAULT_BASE_COLOR = "#7f7f7f"         # Grau für unbekannte RMWs

# Alle Unterordner im Messverzeichnis ermitteln
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

# 3. Alle Ordner zusammen einlesen
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

# 5. Diagramme pro Sensortyp generieren
for sensor_type in df["Sensor"].unique():
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

    fig_width = max(9, len(rmw_order) * max(2.2, num_runs * 0.7))
    fig, ax = plt.subplots(figsize=(fig_width, 6.5))
    
    barplot = sns.barplot(
        data=df_filtered,
        x="RMW Implementation",
        y="Gesamtzeit (ms)",
        hue="Durchlauf (Ordner)",
        order=rmw_order,
        ax=ax
    )
    
    # Legende entfernen
    if ax.get_legend() is not None:
        ax.get_legend().remove()
    
    # Einheitliche RMW-Farben mit feiner dunkler Kontur
    for run_idx in range(num_runs):
        for rmw_idx, rmw_name in enumerate(rmw_order):
            base_col = RMW_BASE_COLORS.get(rmw_name, DEFAULT_BASE_COLOR)
            
            patch_idx = run_idx * len(rmw_order) + rmw_idx
            if patch_idx < len(barplot.patches):
                patch = barplot.patches[patch_idx]
                patch.set_facecolor(base_col)
                patch.set_edgecolor("#222222")
                patch.set_linewidth(0.8)

    # Nur der prägnante Haupttitel (zentriert)
    plt.title(
        f"ROS 2 Performance-Benchmark: {sensor_type}-Daten",
        fontsize=14,
        fontweight='bold',
        pad=15
    )
    
    plt.xlabel("Middleware-Implementierung (RMW)", fontsize=11, fontweight='semibold', labelpad=12)
    plt.ylabel("Gesamtlaufzeit [ms]", fontsize=11, fontweight='semibold', labelpad=12)
    plt.xticks(rotation=15, ha='right', fontsize=10)
    
    # Zahlenwerte über den Balken
    for p in barplot.patches:
        height = p.get_height()
        if height > 0:
            formatted_val = f"{height:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")
            barplot.annotate(
                f"{formatted_val} ms",
                (p.get_x() + p.get_width() / 2., height),
                ha='center', va='bottom',
                xytext=(0, 4), 
                textcoords='offset points', 
                fontsize=8,
                fontweight='semibold',
                rotation=45
            )
            
    # Y-Achse nach oben leicht erweitern, damit Labels nicht abgeschnitten werden
    ax.set_ylim(top=ax.get_ylim()[1] * 1.12)
    
    plt.tight_layout()
    
    # 6. Bild speichern
    output_filename = f"benchmark_{sensor_type.lower()}_by_rmw.png"
    save_path = os.path.join(image_output_dir, output_filename)
    
    plt.savefig(save_path, dpi=300)
    plt.close(fig)
    
    print(f"Diagramm gespeichert: {save_path}")