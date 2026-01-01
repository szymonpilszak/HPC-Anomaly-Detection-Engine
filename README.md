# HPC Anomaly Detection Engine (C + Python)

A high-performance system for real-time signal analysis and anomaly detection. This project demonstrates a hybrid architecture combining the raw computational power of **C** with the flexibility and advanced visualization of **Python**.

## 🚀 Performance Highlights

The system is optimized for massive datasets (10M+ records), achieving industry-leading throughput:
- **Core Engine Speed:** ~725,000,000 samples per second.
- **Latency:** Sub-10ms for 10 million data points.
- **I/O Optimization:** Zero-copy memory mapping (`mmap`) reduces data load time from 20s (CSV) to <1ms (NPY).

## 🛠 Technology Stack
- **Computational Core:** C (Z-Score algorithm, OpenMP parallelization).
- **Bridge Layer:** Python (ctypes, NumPy).
- **Data Engineering:** Memory-mapped I/O, Binary Persistence (NPY).
- **Analytics:** Pandas (for legacy CSV support), Matplotlib (HPC-grade visualization).

## 📊 Visual Validation

The system employs a statistical approach (3rd Sigma Rule) to identify outliers. The visualization engine is specifically tuned to maintain clarity even when handling extreme signal spikes:

| Feature | Description |
| :--- | :--- |
| **Statistical Boundaries** | Green dashed lines represent $\pm 3\sigma$ decision thresholds. |
| **Contextual Scaling** | Automatic Y-axis clipping ensures noise visibility while highlighting anomalies. |
| **Real-Time Telemetry** | In-plot reporting of throughput, count, and execution time. |

## 📂 Project Structure
- `engine.c`: C source for the detection algorithm.
- `bridge.py`: Python interface and visualization engine.
- `data_gen.py`: High-speed data generator for NPY and CSV formats.
- `engine.dll`: Compiled shared library.

## ⚙️ Quick Start

### 1. Requirements
```bash```
pip install -r requirements.txt


### 2. Generate Data
python data_gen.py
# Recommended: 10,000,000 records, save as .npy

### 3. Run Analysis
python data_gen.py
# Recommended: 10,000,000 records, save as .npy
