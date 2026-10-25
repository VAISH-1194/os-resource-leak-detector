"""Recovery actions for simulation mode only."""


def simulated_reset(memory_samples_mb, reset_to_mb=None):
    """Return a new sample list whose last value is reset to a safe demo value.

    This function does not touch OS processes or real system memory.
    """
    samples = list(memory_samples_mb)
    if not samples:
        return samples

    target = reset_to_mb if reset_to_mb is not None else samples[0]
    samples[-1] = min(samples[-1], target)
    return samples
