"""Starter heuristic for flagging suspicious simulated memory growth."""


def detect_suspicious_growth(
    memory_samples_mb,
    minimum_growth_mb=150,
    minimum_consecutive_increases=3,
):
    """Flag a series when growth and consecutive increases meet chosen thresholds.

    This is an educational heuristic, not proof of a true resource leak.
    """
    samples = list(memory_samples_mb)
    if len(samples) < 2:
        return {
            "suspicious": False,
            "total_growth_mb": 0 if not samples else 0,
            "consecutive_increases": 0,
            "reason": "Not enough samples",
        }

    total_growth = samples[-1] - samples[0]
    consecutive_increases = 0
    longest_run = 0

    for previous, current in zip(samples, samples[1:]):
        if current > previous:
            consecutive_increases += 1
            longest_run = max(longest_run, consecutive_increases)
        else:
            consecutive_increases = 0

    suspicious = (
        total_growth >= minimum_growth_mb
        and longest_run >= minimum_consecutive_increases
    )

    return {
        "suspicious": suspicious,
        "total_growth_mb": total_growth,
        "consecutive_increases": longest_run,
        "reason": (
            "Growth and trend conditions met"
            if suspicious
            else "Selected conditions not met"
        ),
    }
