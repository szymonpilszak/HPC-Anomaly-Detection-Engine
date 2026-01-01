import ctypes
import numpy as np
import pandas as pd
import time
import os
import matplotlib.pyplot as plt

# 

class AnomalyEngine:
    def __init__(self, lib_path='engine.dll'):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current_dir, lib_path)
        if hasattr(os, 'add_dll_directory'):
            os.add_dll_directory(current_dir)
            
        try:
            self.lib = ctypes.CDLL(path, winmode=0)
            self.lib.detect_anomalies.argtypes = [
                np.ctypeslib.ndpointer(dtype=np.float64),
                np.ctypeslib.ndpointer(dtype=np.int32),
                ctypes.c_int,
                ctypes.c_double
            ]
            self.lib.detect_anomalies.restype = ctypes.c_int
        except Exception as e:
            raise RuntimeError(f"FATAL: Library load failed: {e}")

    def run(self, data):
        # Ensure contiguous memory for C-pointer interoperability
        data_c = np.ascontiguousarray(data.flatten(), dtype=np.float64)
        results = np.zeros(len(data_c), dtype=np.int32)
        
        start = time.perf_counter()
        self.lib.detect_anomalies(data_c, results, len(data_c), 3.0) # Threshold = 3.0
        duration = time.perf_counter() - start
        
        return results, duration

if __name__ == "__main__":
    engine = AnomalyEngine()
    print("\n[ HPC Anomaly Detection System ]")
    path = input("Enter file path (data.npy or data.csv) or press Enter for auto-gen: ").strip()

    # --- PHASE 1: Data Ingestion ---
    start_io = time.perf_counter()
    if path and os.path.exists(path):
        if path.endswith('.npy'):
            print(f"[*] Mode: Binary NPY (Zero-Copy mmap)")
            data = np.load(path, mmap_mode='r')
            method = "NumPy mmap"
        else:
            print(f"[*] Mode: CSV (Pandas Engine)")
            df = pd.read_csv(path)
            # Ensure we extract the numerical column
            data = df.iloc[:, 0].values.astype(np.float64)
            method = "Pandas CSV"
    else:
        print("[*] Mode: Synthetic Generation (RAM)")
        data = np.random.normal(0, 1, 10_000_000).astype(np.float64)
        data[7] = 999.9 # Test anomaly
        method = "Random Gen"
    
    io_time = time.perf_counter() - start_io

    # --- PHASE 2: Core Analysis ---
    results, engine_time = engine.run(data)
    anomaly_indices = np.where(results == 1)[0]

    # --- PHASE 3: Professional Telemetry ---
    print(f"\n" + "="*30)
    print(f" PERFORMANCE METRICS ({method})")
    print(f"="*30)
    print(f"I/O Load:     {io_time:.4f}s")
    print(f"C-Engine:     {engine_time:.4f}s")
    print(f"Throughput:   {len(data)/engine_time:,.0f} pts/sec")
    print(f"Anomalies:    {len(anomaly_indices)}")
    print(f"="*30)

    # --- PHASE 4: Report Generation (THE MISSING PART) ---
    if len(anomaly_indices) > 0:
        report_path = "anomalies_report.csv"
        print(f"\n[*] Exporting forensic report to {report_path}...")
        
        # Combine indices and actual values of anomalies
        # We use data[anomaly_indices] to get the values from the original array
        report_data = np.column_stack((anomaly_indices, data[anomaly_indices]))
        
        np.savetxt(report_path, report_data, delimiter=",", 
                   header="Index,Value", comments="", fmt=["%d", "%.6f"])
        print(f"[SUCCESS] Found {len(anomaly_indices)} anomalies. File ready.")
    else:
        print("\n[*] No anomalies detected. Report skipped.")

 # --- PHASE 5: Professional Visualization ---
    limit = min(len(data), 2000)
    plt.figure(figsize=(14, 8), facecolor='#f8f9fa')
    
    # Tworzymy dwa podwykresy (Subplots) lub jeden z ograniczoną osią
    ax = plt.gca()
    
    # 1. Główny sygnał
    plt.plot(data[:limit], alpha=0.6, label="Sensor Signal (Raw)", color='#1f77b4', linewidth=1)
    
    # 2. Anomalie
    view_anomalies = anomaly_indices[anomaly_indices < limit]
    if len(view_anomalies) > 0:
        plt.scatter(view_anomalies, data[view_anomalies], 
                    color='red', s=60, label="Detected Outliers", 
                    edgecolor='black', zorder=5)
    
    # 3. Dynamiczne progi (Z-Score)
    mean_val = np.mean(data)
    std_val = np.std(data)
    plt.axhline(y=mean_val + 3*std_val, color='green', linestyle='--', alpha=0.8, label='Upper Threshold (+3σ)')
    plt.axhline(y=mean_val - 3*std_val, color='green', linestyle='--', alpha=0.8, label='Lower Threshold (-3σ)')
    
    # --- KLUCZOWA POPRAWKA: OGRANICZENIE OSI Y ---
    # Ustawiamy widok tak, aby było widać szum, ale anomalia "wystrzeliła" w górę
    # Jeśli anomalia jest gigantyczna (np. 1000), tniemy widok do sensownego poziomu
    y_max = max(mean_val + 10 * std_val, 10) 
    y_min = min(mean_val - 10 * std_val, -10)
    plt.ylim(y_min, y_max) 
    # Dzięki temu progi będą wyraźne, a anomalia będzie wskazywać poza skalę lub na jej szczyt
    
    # 4. Opisy
    plt.title("HPC Engine: Real-Time Signal Analysis", fontsize=16, fontweight='bold')
    plt.xlabel("Sample Index (Time Domain)", fontsize=12)
    plt.ylabel("Signal Magnitude (Normalized)", fontsize=12)
    
    # 5. Estetyka
    plt.grid(True, which='both', linestyle=':', alpha=0.6)
    plt.legend(loc='upper right', frameon=True, shadow=True)
    
    # Telemetria w rogu
    stats = f"Total Pts: {len(data):,}\nAnomalies: {len(anomaly_indices)}\nEngine Time: {engine_time:.4f}s"
    plt.text(0.02, 0.98, stats, transform=ax.transAxes, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.9), size=10, family='monospace')

    print("\n[*] Rendering visualization...")
    plt.tight_layout()
    plt.show()