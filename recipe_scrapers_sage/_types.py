"""Custom Types."""

from datetime import datetime, timedelta
from typing import Literal, Union

JSON_LD = dict
ISO8601_Date = str
Date = Union[ISO8601_Date, datetime]
URL = str
ISO8601_Duration = str  # ISO8601Time https://en.wikipedia.org/wiki/ISO_8601#Durations
Duration = Union[ISO8601_Duration, timedelta]
InstructionType = Union[Literal["HowToSection"], Literal["HowToStep"]]
