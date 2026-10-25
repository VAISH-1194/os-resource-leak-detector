
"""Bounded workload for real Codespace monitoring.

This is a test workload, not a real memory leak.
Maximum allocation: 64 MB.
Maximum runtime: 90 seconds.
"""

import os
import time

CHUNK_MB = 2
MAX_MEMORY_MB = 64
INTERVAL_SECONDS = 2
MAX_RUNTIME_SECONDS = 600


def main():
    allocations = []
    started = time.monotonic()

    print(f"Workload PID: {os.getpid()}", flush=True)
    print("Mode: controlled memory growth", flush=True)

    try:
        while (
            time.monotonic() - started < MAX_RUNTIME_SECONDS
            and len(allocations) * CHUNK_MB < MAX_MEMORY_MB
        ):
            # Allocate and retain a small amount of real process memory.
            allocations.append(bytearray(CHUNK_MB * 1024 * 1024))

            current_mb = len(allocations) * CHUNK_MB
            print(f"Allocated test memory: {current_mb} MB", flush=True)

            time.sleep(INTERVAL_SECONDS)

        print("Allocation limit or time limit reached.", flush=True)
        time.sleep(10)

    except KeyboardInterrupt:
        print("Workload stopped by user.", flush=True)

    finally:
        allocations.clear()
        print("Test allocations released.", flush=True)


if __name__ == "__main__":
    main()
