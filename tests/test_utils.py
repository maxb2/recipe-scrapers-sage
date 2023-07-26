from datetime import timedelta

import pytest

from recipe_scrapers_sage.utils import simple_ISO8601_duration


def test_util():
    assert simple_ISO8601_duration("P0.0Y0.0M0.0DT1.5H15.5M2.5S") == "PT1H45M32S"

    assert (
        simple_ISO8601_duration(
            timedelta(days=1.5, hours=1.1, minutes=30.1, seconds=30.1)
        )
        == "PT37H36M36S"
    )

    with pytest.raises(ValueError, match="not a valid ISO8601_Duration"):
        simple_ISO8601_duration("bad")

    with pytest.raises(ValueError, match="not a valid Duration"):
        simple_ISO8601_duration(10)
