"""Small deterministic data generator for experiments."""


def make_demo_processes():
    """Return example process names mapped to memory measurements in MB.

    Values are intentionally simulated, not collected from a real operating system.
    """
    return {
        "Process_A": [100, 104, 102, 105, 103, 106],
        "Process_B": [100, 145, 205, 270, 335, 410],
        "Process_C": [100, 180, 125, 115, 120, 118],
    }
