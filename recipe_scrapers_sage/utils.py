"""Utilities."""

import re
from datetime import timedelta

from ._types import Duration, ISO8601_Duration

ISO8601_DURATION_REGEX = re.compile(
    r"^P(?!$)"
    r"(?P<PY>\d+(?:\.\d+)?Y)?"
    r"(?P<PM>\d+(?:\.\d+)?M)?"
    r"(?P<PW>\d+(?:\.\d+)?W)?"
    r"(?P<PD>\d+(?:\.\d+)?D)?"
    r"(T(?=\d)"
    r"(?P<TH>\d+(?:\.\d+)?H)?"
    r"(?P<TM>\d+(?:\.\d+)?M)?"
    r"(?P<TS>\d+(?:\.\d+)?S)?"
    r")?$"
)


def simple_ISO8601_duration(duration: Duration) -> ISO8601_Duration:
    """Create a simple ISO8601 Duration importable by RecipeSage.

    Notes: RecipeSage only allows the `PT<N.NH><N.NM><N.NS>` format.
        See [here](https://github.com/julianpoy/RecipeSage/blob/679a177f19d2f7be2aadaab50c3e8c3b4c4d7b94/packages/backend/src/services/json-ld.js#L151-L157).

    Args:
        duration (Duration): duration to format

    Returns:
        ISO8601_Duration: simple duration
    """

    def seconds_to_ISO8601_duration(_time: int) -> ISO8601_Duration:
        out = "PT"
        seconds = _time % 60
        _time = _time // 60
        minutes = _time % 60
        hours = _time // 60
        if hours > 0:
            out += f"{hours}H"
        if minutes > 0:
            out += f"{minutes}M"
        if seconds > 0:
            out += f"{seconds}S"
        return out

    if isinstance(duration, timedelta):
        return seconds_to_ISO8601_duration(int(duration.total_seconds()))

    if isinstance(duration, str):
        _match = ISO8601_DURATION_REGEX.match(duration)
        if _match:
            _time = 0.0
            _time += float((_match.groupdict().get("TS") or "0").strip("S"))
            _time += float((_match.groupdict().get("TM") or "0").strip("M")) * 60
            _time += float((_match.groupdict().get("TH") or "0").strip("H")) * 3600
            _time = int(_time)

            return seconds_to_ISO8601_duration(_time)
        message = f"not a valid ISO8601_Duration: {duration}"
        raise ValueError(message)
    message = f"not a valid Duration: {duration}"
    raise ValueError(message)
