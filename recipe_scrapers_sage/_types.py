"""Custom Types."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Literal, Union

if TYPE_CHECKING:  # pragma: no cover
    import sys

    if sys.version_info > (3, 9):
        from typing import TypeAlias
    else:
        from typing_extensions import TypeAlias


JSON_LD: TypeAlias = dict
ISO8601_Date: TypeAlias = str
Date: TypeAlias = Union[ISO8601_Date, datetime]
URL: TypeAlias = str
# ISO8601Time https://en.wikipedia.org/wiki/ISO_8601#Durations
ISO8601_Duration: TypeAlias = str
Duration: TypeAlias = Union[ISO8601_Duration, timedelta]
InstructionType: TypeAlias = Union[Literal["HowToSection"], Literal["HowToStep"]]
