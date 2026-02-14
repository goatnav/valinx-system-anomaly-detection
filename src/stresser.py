import math
import os
import time
import tempfile
import requests
import multiprocessing as mp
import numpy as np
import psutil

# =====================================================
# 🔧 Helper: worker for CPU stress (must be top-level!)
# =====================================================
def _burn(_):
    """Worker function for CPU stress."""
    x = 0.0
    for _ in range(10_000_000):
        x += math.sqrt(12345.6789)


# =====================================================
# 🔥 CPU Stress
# =====================================================
def stress_cpu(duration=30):
    """Use multiple processes to peg the CPU."""
    print(f"🔥 Stressing CPU for {duration}s...")

    n_procs = max(1, psutil.cpu_count(logical=True) - 1)  # leave one core free
    pool = mp.Pool(n_procs)
    start = time.time()

    try:
        while time.time() - start < duration:
            pool.map(_burn, range(n_procs))
    except KeyboardInterrupt:
        print("🛑 CPU stress interrupted by user.")
    finally:
        pool.terminate()
        pool.join()

    print("✅ CPU stress done.")


# =====================================================
# 💾 Memory Stress
# =====================================================
def stress_memory(duration=30, size_mb=500):
    """Allocate and repeatedly touch a large block of memory."""
    print(f"💾 Stressing memory ({size_mb} MB) for {duration}s...")

    try:
        arr = np.ones((size_mb * 250_000,), dtype=np.float32)  # ~1 MB per 250k elements
    except MemoryError:
        print("⚠️ Not enough memory! Try a smaller size_mb.")
        return

    start = time.time()
    try:
        while time.time() - start < duration:
            arr *= 1.000001  # tiny operation keeps it hot in RAM
    except KeyboardInterrupt:
        print("🛑 Memory stress interrupted.")
    finally:
        del arr

    print("✅ Memory stress done.")


# =====================================================
# 💽 Disk Stress
# =====================================================
def stress_disk(duration=30, file_size_mb=200):
    """Write and read a temporary file repeatedly."""
    print(f"💽 Stressing disk with {file_size_mb} MB file for {duration}s...")

    temp_dir = tempfile.gettempdir()
    path = os.path.join(temp_dir, "valinx_stress.tmp")
    block = os.urandom(1024 * 1024)  # 1 MB random block

    start = time.time()
    try:
        with open(path, "wb") as f:
            for _ in range(file_size_mb):
                f.write(block)

        while time.time() - start < duration:
            with open(path, "rb") as f:
                _ = f.read()
    except KeyboardInterrupt:
        print("🛑 Disk stress interrupted.")
    finally:
        if os.path.exists(path):
            os.remove(path)

    print("✅ Disk stress done.")


# =====================================================
# 🌐 Network Stress
# =====================================================
def stress_network(duration=30, url="https://speed.hetzner.de/100MB.bin"):
    """
    Download a file repeatedly to generate network load.
    Default: Hetzner public 100 MB file.
    """
    print(f"🌐 Stressing network for {duration}s from {url}")
    start = time.time()

    try:
        while time.time() - start < duration:
            r = requests.get(url, stream=True, timeout=10)
            for _ in r.iter_content(chunk_size=1024 * 1024):
                if time.time() - start > duration:
                    break
    except KeyboardInterrupt:
        print("🛑 Network stress interrupted.")
    except Exception as e:
        print("⚠️ Network stress error:", e)
        time.sleep(3)

    print("✅ Network stress done.")


# =====================================================
# 🚀 Combined Stress (optional)
# =====================================================
def stress_all(duration=30):
    """Run CPU, Memory, and Disk stressors in parallel."""
    print(f"🚀 Stressing all subsystems for {duration}s...")

    procs = []
    for func in (stress_cpu, stress_memory, stress_disk):
        p = mp.Process(target=func, args=(duration,))
        p.start()
        procs.append(p)

    try:
        for p in procs:
            p.join()
    except KeyboardInterrupt:
        print("🛑 Combined stress interrupted.")
        for p in procs:
            p.terminate()
    print("✅ All-subsystem stress done.")


# =====================================================
# 🧩 Safe Preset Mode (optional)
# =====================================================
def stress_safe():
    """Run each stressor briefly with safe defaults."""
    print("🧠 Running safe preset stress (10s each, moderate load)...")
    stress_cpu(10)
    stress_memory(10, size_mb=300)
    stress_disk(10, file_size_mb=100)
    stress_network(10)
    print("✅ Safe preset complete.")


# =====================================================
# 📋 CLI Menu
# =====================================================
if __name__ == "__main__":
    print("\nVALinX Stress Tester")
    print("=======================")
    print("1) CPU\n2) Memory\n3) Disk\n4) Network\n5) All\n6) Safe preset\n")

    choice = input("Select stress type (1-6): ").strip()
    dur = int(input("Duration in seconds (default=30): ") or "30")

    if choice == "1":
        stress_cpu(dur)
    elif choice == "2":
        size = int(input("Memory size in MB (default=500): ") or "500")
        stress_memory(dur, size)
    elif choice == "3":
        size = int(input("Disk file size in MB (default=200): ") or "200")
        stress_disk(dur, size)
    elif choice == "4":
        stress_network(dur)
    elif choice == "5":
        stress_all(dur)
    elif choice == "6":
        stress_safe()
    else:
        print("Invalid choice.")
