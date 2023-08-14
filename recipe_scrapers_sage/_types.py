"""Custom Types."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Literal

JSON_LD = dict
ISO8601_Date = str
Date = ISO8601_Date | datetime
URL = str
ISO8601_Duration = str  # ISO8601Time https://en.wikipedia.org/wiki/ISO_8601#Durations
Duration = ISO8601_Duration | timedelta
InstructionType = Literal["HowToSection"] | Literal["HowToStep"]
