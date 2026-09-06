def format_clock(ms: int) -> str:
    if ms < 0:
        ms = 0
    total_seconds = int(ms / 1000)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    return f"{minutes}:{seconds:02d}"


def format_remaining(position_ms: int, duration_ms: int) -> str:
    remaining = max(0, duration_ms - position_ms)
    return f"-{format_clock(remaining)}"
