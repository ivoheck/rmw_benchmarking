import os
import glob
import re
import pandas as pd
import numpy as np

# 1. Pfade definieren
script_dir = os.path.dirname(os.path.abspath(__file__))
base_measurement_dir = os.path.join(script_dir, "../messurement")
output_dir = os.path.join(script_dir, "reproducibility_results")
os.makedirs(output_dir, exist_ok=True)

if not os.path.exists(base_measurement_dir):
    print(f"Fehler: '{base_measurement_dir}' existiert nicht!")
    exit(1)

subfolders = [
    os.path.join(base_measurement_dir, d) 
    for d in os.listdir(base_measurement_dir) 
    if os.path.isdir(os.path.join(base_measurement_dir, d))
]

# 2. Rohdaten einlesen (Warm-up von 10 Datenpunkten überspringen)
all_raw_data = []
NUM_HOPS = 6  # Publisher -> 5 Zwischenknoten -> Subscriber = 6 Hops

for folder_path in sorted(subfolders):
    folder_name = os.path.basename(folder_path)
    txt_files = glob.glob(os.path.join(folder_path, '*.txt'))

    for file_path in txt_files:
        file_name = os.path.basename(file_path)
        
        match = re.match(r"([a-zA-Z0-9]+)_cpp_results_(rmw_[a-zA-Z0-9_]+?)_nr_\d+\.txt", file_name)
        if not match:
            continue  
            
        sensor_type = match.group(1).upper() if match.group(1).lower() == "imu" else match.group(1).capitalize()
        rmw_name = match.group(2)
        
        total_nanoseconds = 0
        valid_samples = 0
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                entry_count = 0
                for line in file:
                    cleaned_line = line.strip()
                    if not cleaned_line:
                        continue
                    
                    entry_count += 1
                    if entry_count <= 50:
                        continue  # Warm-up überspringen
                    
                    number_part = cleaned_line.split()[0]
                    total_nanoseconds += int(number_part)
                    valid_samples += 1
                    
            total_milliseconds = total_nanoseconds / 1_000_000
            
            all_raw_data.append({
                "Durchlauf": folder_name,
                "Sensor": sensor_type,
                "RMW": rmw_name,
                "Gesamtzeit_ms": total_milliseconds,
                "Samples": valid_samples
            })
        except Exception as e:
            print(f"Fehler beim Parsen von {file_name}: {e}")

df_raw = pd.DataFrame(all_raw_data)

if df_raw.empty:
    print("Keine Daten gefunden!")
    exit(0)

# Aggregation pro Durchlauf
df_runs = df_raw.groupby(["Sensor", "RMW", "Durchlauf"], as_index=False).agg({
    "Gesamtzeit_ms": "sum",
    "Samples": "sum"
})

# 3. Metriken zur Reproduzierbarkeit und Einzellatenzen berechnen
def compute_metrics(group):
    n = len(group)
    mean_total = group["Gesamtzeit_ms"].mean()
    std_val = group["Gesamtzeit_ms"].std(ddof=1) if n > 1 else 0.0
    cv_percent = (std_val / mean_total * 100) if mean_total > 0 else 0.0
    spread_rel = ((group["Gesamtzeit_ms"].max() - group["Gesamtzeit_ms"].min()) / mean_total * 100) if mean_total > 0 else 0.0
    
    # Durchschnittliche Anzahl an Samples pro Run ermitteln
    avg_samples = group["Samples"].mean()
    
    # Latenz pro einzelner Nachricht (Ende-zu-Ende über die Kette)
    e2e_per_msg_ms = (mean_total / avg_samples) if avg_samples > 0 else 0.0
    
    # Latenz pro einzelnem Hop (geteilt durch 6)
    hop_per_msg_ms = e2e_per_msg_ms / NUM_HOPS

    return pd.Series({
        "Runs (N)": int(n),
        "Samples": int(avg_samples),
        "Mittelwert [ms]": round(mean_total, 2),
        "Latenz Kette [ms]": round(e2e_per_msg_ms, 4),
        "Latenz Hop [ms]": round(hop_per_msg_ms, 4),
        "CV [%]": round(cv_percent, 2),
        "Spanne Rel [%]": round(spread_rel, 2)
    })

reproducibility_df = df_runs.groupby(["Sensor", "RMW"]).apply(compute_metrics, include_groups=False).reset_index()

# 4. Sortieren
reproducibility_df = reproducibility_df.sort_values(by=["Sensor", "CV [%]"], ascending=[True, True])

# 5. Konsolenausgabe
print("\n" + "="*110)
print("             REPRODUZIERBARKEITS- UND LATENZANALYSE DER BENCHMARKS")
print("="*110)
print(reproducibility_df.to_string(index=False))
print("="*110)

# 6. CSV speichern
csv_path = os.path.join(output_dir, "reproducibility_report.csv")
reproducibility_df.to_csv(csv_path, index=False, sep=";")
print(f"\nErgebnis erfolgreich als CSV gespeichert: {csv_path}")

# --- Typst Export Block im Python Skript ---
typst_path = os.path.join(output_dir, "reproducibility_report.typ")

with open(typst_path, "w", encoding="utf-8") as f:
    f.write("#figure(\n")
    f.write("  placement: auto,\n")
    f.write('  scope: "parent",\n')
    f.write("  table(\n")
    f.write(
        "    columns: (auto, auto, auto, auto, 1fr, 1fr, 1fr, 1fr, 1fr),\n"
    )
    f.write(
        "    stroke: (x, y) => if y == 0 { (bottom: 1pt + black) } else if y"
        " == 1 { (bottom: 0.5pt + black) } else { none },\n"
    )
    f.write("    table.header(\n")
    f.write(
        "      [*Sensor*], [*RMW*], [*Runs*], [*Samples*], [*Mittelwert [ms]*],"
        " [*Kette [ms]*], [*Hop [ms]*], [*CV [%]*], [*Spanne [%]*]\n"
    )
    f.write("    ),\n")

    for _, row in reproducibility_df.iterrows():
        rmw_clean = f"`{row['RMW']}`"
        f.write(
            f"    [{row['Sensor']}], {rmw_clean}, [{int(row['Runs (N)'])}],"
            f" [{int(row['Samples'])}], [{row['Mittelwert [ms]']:,.2f}],"
            f" [{row['Latenz Kette [ms]']:.4f}],"
            f" [{row['Latenz Hop [ms]']:.4f}], [{row['CV [%]']:.2f}\\%],"
            f" [{row['Spanne Rel [%]']:.2f}\\%],\n"
        )

    f.write("  ),\n")
    f.write(
        "  caption: [Reproduzierbarkeits- und Latenzanalyse über 3 Testläufe (6"
        " Hops)],\n"
    )
    f.write(")\n")

#TODO: hier immer die selbe reihenvollge der middleware verwenden