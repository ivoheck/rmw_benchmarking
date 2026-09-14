import os
import glob
import re
import pandas as pd
import numpy as np

# 1. Pfade definieren
script_dir = os.path.dirname(os.path.abspath(__file__))
base_measurement_dir = os.path.join(script_dir, "../messurement")
output_csv_path = os.path.join(script_dir, "warmup_and_convergence_results.csv")

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

def calculate_convergence_length(values, tolerance=0.05, window=5):
    """Ermittelt ab welchem Messindex (1-based) sich die Werte dauerhaft 
    innerhalb von +/- tolerance des Steady-State-Mittelwerts befinden."""
    if len(values) < window:
        return 0
    # Baseline ist der Mittelwert der zweiten Hälfte der Messung
    baseline = np.mean(values[len(values)//2:])
    if baseline == 0:
        return 0
    lower = baseline * (1 - tolerance)
    upper = baseline * (1 + tolerance)
    
    for i in range(len(values) - window + 1):
        window_vals = values[i:i+window]
        if all(lower <= v <= upper for v in window_vals):
            return i + 1  # 1-basierter Index
    return len(values)

# 2. Alle Einzelwerte einlesen (inkl. Warm-up für die Analyse)
all_file_data = []

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
        
        all_vals = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    cleaned_line = line.strip()
                    if not cleaned_line:
                        continue
                    val_ms = float(cleaned_line.split()[0]) / 1_000_000
                    all_vals.append(val_ms)
            
            if len(all_vals) > 10:
                warmup_vals = all_vals[:10]
                steady_vals = all_vals[10:]
                
                w_mean = np.mean(warmup_vals)
                w_std = np.std(warmup_vals, ddof=1) if len(warmup_vals) > 1 else 0.0
                s_mean = np.mean(steady_vals)
                
                cold_start_ratio = w_mean / s_mean if s_mean > 0 else 0.0
                conv_length = calculate_convergence_length(all_vals, tolerance=0.05, window=5)
                
                all_file_data.append({
                    "Durchlauf": folder_name,
                    "Sensor": sensor_type,
                    "RMW Implementation": rmw_name,
                    "Warmup Mean [ms]": w_mean,
                    "Warmup Std [ms]": w_std,
                    "Steady State Mean [ms]": s_mean,
                    "Cold-Start Ratio": cold_start_ratio,
                    "Convergence Length": conv_length
                })
        except Exception as e:
            print(f"Fehler beim Parsen von {file_name}: {e}")

df_runs = pd.DataFrame(all_file_data)

if df_runs.empty:
    print("Keine auswertbaren Daten gefunden!")
    exit(0)

# 3. Über alle Durchläufe (Macro-Ebene) mitteln
df_summary = df_runs.groupby(["Sensor", "RMW Implementation"], as_index=False).agg({
    "Warmup Mean [ms]": "mean",
    "Warmup Std [ms]": "mean",
    "Steady State Mean [ms]": "mean",
    "Cold-Start Ratio": "mean",
    "Convergence Length": "mean"
}).sort_values(by=["Sensor", "Cold-Start Ratio"], ascending=[True, False])

# Formatierung für saubere Konsolenausgabe
df_summary["Cold-Start Ratio"] = df_summary["Cold-Start Ratio"].round(2)
df_summary["Convergence Length"] = df_summary["Convergence Length"].round(1)

# 4. Ergebnisse ausgeben und speichern
print("\n--- Warm-up, Kaltstart & Konvergenz-Analyse (Mittelwerte über alle Läufe) ---")
print(df_summary.to_string(index=False))

df_summary.to_csv(output_csv_path, index=False, encoding='utf-8')
print(f"\nErgebnisse erfolgreich gespeichert unter: {output_csv_path}")