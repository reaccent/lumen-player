from app.utils.timefmt import format_clock, format_remaining


def test_format_clock_minutes():
    assert format_clock(0) == "0:00"
    assert format_clock(1_500) == "0:01"
    assert format_clock(125_000) == "2:05"


def test_format_clock_hours():
    assert format_clock(3_661_000) == "1:01:01"


def test_format_remaining():
    assert format_remaining(15_000, 90_000) == "-1:15"
