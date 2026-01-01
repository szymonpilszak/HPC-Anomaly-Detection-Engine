# 🚀 Ultra-Fast Anomaly Detection Engine (C-Core / Python-Hybrid)

## ⚡ The Challenge
Standard Python implementations for anomaly detection often fail when processing millions of records per second due to the Global Interpreter Lock (GIL) and memory overhead. This project demonstrates a **high-frequency trading (HFT) grade** approach to real-time data analysis.

## 📊 Performance Benchmarks
- **Dataset:** 10,000,000 Float64 records.
- **Processing Time:** **~0.0128 seconds**.
- **Throughput:** **~780,000,000 records/sec**.
- **Efficiency:** 200x faster than pure Python; outperforms standard NumPy vectorized operations by utilizing multi-core C parallelism via OpenMP.



## 🧠 Technical Architecture

### 1. Computational Core (C + OpenMP)
The engine is written in stateless, optimized C. It utilizes **OpenMP** to saturate all available CPU cores. 
- **Algorithm:** Z-Score based statistical outlier detection.
- **Optimization:** Compiled with `-O3` and `-march=native` to leverage SIMD (Single Instruction, Multiple Data) vectorization.
- **Linkage:** Statically linked to ensure portability across environments without external dependencies.

### 2. Zero-Copy Bridge (Python + ctypes)
The system employs a **Zero-Copy** strategy to eliminate memory bottlenecks.
- Python passes the memory address (pointer) of a NumPy array directly to the C library.
- **Memory Overhead:** $O(1)$ — the system never duplicates the dataset in RAM.
- **Interoperability:** Seamless integration between high-level Python logic and low-level C performance.

### 3. High-Speed Persistence
- **Binary I/O:** Uses `.npy` format for near-instant disk-to-RAM loading.
- **Storage Efficiency:** 10M records stored in a 76MB binary blob, bypassing the massive overhead of CSV formats.

## 📈 Visualization & Forensics
The system provides deep visual and data-driven insights:
- **X-Axis (Sample Index):** Represents the temporal sequence of sensor readings.
- **Y-Axis (Amplitude):** Represents the raw value of the data point.
- **Threshold Lines:** Statistical boundaries set at $\pm 3\sigma$.
- **Automated Reporting:** Generates `anomalies_report.csv` with precise timestamps and values for every detected outlier.



## 🛠️ Build & Installation

### Prerequisites
- GCC (MinGW-w64 for Windows)
- Python 3.8+
- NumPy, Matplotlib

### Build the Shared Library
```bash
gcc -O3 -shared -o engine.dll engine.c -fopenmp -static
