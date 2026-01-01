import numpy as np
import time
import os

def generate_all_formats():
    n = 10_000_000
    print(f"[*] Generating {n:,} records...")
    data = np.random.normal(0, 1, n).astype(np.float64)
    data[500] = 999.9

    # 1. Zapis BINARNY (Dla profesjonalistów)
    start = time.perf_counter()
    np.save("data.npy", data)
    print(f"[+] Saved NPY in {time.perf_counter()-start:.4f}s (Rozmiar: ~76MB)")

    # 2. Zapis CSV (Dla porównania - zobaczysz jaki to muł)
    choice = input("[?] Generate CSV too? (Slow!) [y/n]: ")
    if choice.lower() == 'y':
        start = time.perf_counter()
        # Zapisujemy tylko 1M do CSV, bo 10M zajmie wieczność
        np.savetxt("data.csv", data[:1000000], delimiter=",", header="Value")
        print(f"[+] Saved CSV (1M records) in {time.perf_counter()-start:.4f}s")

if __name__ == "__main__":
    generate_all_formats()