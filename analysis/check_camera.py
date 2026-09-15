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

if not os.path.exists(base_measurement_dir):
    print(f"Fehler: Das Verzeichnis '{base_measurement_dir}' existiert nicht!")
    exit(1)

subfolders = [
    os.path.join(base_measurement_dir, d) 
    for d in os.listdir(base_measurement_dir) 
    if os.path.isdir(os.path.join(base_measurement_dir, d))
]

# 2. ALLE Rohdaten für alle Sensoren und RMWs einlesen
plot_data = []

for folder_path in sorted(subfolders):
    folder_name = os.path.basename(folder_path)
    txt_files = glob.glob(os.path.join(folder_path, '*.txt'))

    for file_path in txt_files:
        file_name = os.path.basename(file_path)
        
        match = re.match(r"([a-zA-Z0-9]+)_cpp_results_(rmw_[a-zA-Z0-9_]+?)_nr_(\d+)\.txt", file_name)
        if not match:
            continue
            
        sensor_type = match.group(1).upper() if match.group(1).lower() in ["imu"] else match.group(1).capitalize()
        rmw_name = match.group(2)
        run_id = match.group(3)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                sample_idx = 0
                for line in file:
                    cleaned_line = line.strip()
                    if not cleaned_line:
                        continue
                    sample_idx += 1
                    val_ms = float(cleaned_line.split()[0]) / 1_000_000
                    
                    plot_data.append({
                        "Sensor": sensor_type,
                        "RMW Implementation": rmw_name,
                        "Run": f"Run {run_id}",
                        "Sample Index": sample_idx,
                        "Latenz [ms]": val_ms
                    })
        except Exception as e:
            print(f"Fehler beim Parsen von {file_name}: {e}")

df_plot = pd.DataFrame(plot_data)

if df_plot.empty:
    print("Keine Daten gefunden!")
    exit(0)

# 3. Multi-Panel-Plot (FacetGrid) erstellen
sns.set_theme(style="whitegrid")

# Wir nutzen ein Raster: Zeilen = Sensoren, Spalten = RMWs
# sharey=False ist wichtig, da IMU (ms-Bereich) und Kamera (Sekunden-Bereich) völlig andere Skalen haben!
g = sns.FacetGrid(
    df_plot, 
    row="Sensor", 
    col="RMW Implementation", 
    sharey=False, 
    sharex=True,
    height=3, 
    aspect=1.3
)

# Einzelläufe als dünne, halbtransparente Linien einzeichnen
g.map_dataframe(
    sns.lineplot, 
    x="Sample Index", 
    y="Latenz [ms]", 
    hue="Run", 
    alpha=0.25, 
    palette="Blues", 
    legend=False
)

# Mittelwert-Trend als kräftige Linie darüberlegen
def plot_mean(*args, **kwargs):
    data = kwargs.pop("data")
    mean_df = data.groupby("Sample Index")["Latenz [ms]"].mean().reset_index()
    plt.plot(mean_df["Sample Index"], mean_df["Latenz [ms]"], color="darkblue", linewidth=2)

g.map_dataframe(plot_mean)

# Beschriftungen und Layout anpassen
g.set_axis_labels("Sample-Index (Zeit)", "Latenz [ms]")
g.fig.suptitle("Umfassende Kaltstart-Analyse über alle Sensoren und RMWs", y=1.03, fontsize=14, fontweight='bold')

g.tight_layout()

# 4. Speichern
save_path = os.path.join(image_output_dir, "all_sensors_rmw_coldstart_grid.png")
g.savefig(save_path, dpi=300, bbox_inches='tight')
plt.close()

print(f"\nGesamt-Grid erfolgreich gespeichert unter: {save_path}")