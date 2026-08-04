"""Engine configuration validation tests."""

from typing import cast

import pytest
from hypothesis import given
from hypothesis import strategies as st

from ludoweave import EngineConfig
from ludoweave.core.errors import ConfigurationError


def test_default_configuration_uses_sixty_hertz() -> None:
    assert EngineConfig().fixed_hz == 60


@given(st.integers(max_value=0))
def test_non_positive_fixed_hz_is_rejected(fixed_hz: int) -> None:
    with pytest.raises(ConfigurationError, match="greater than zero"):
        EngineConfig(fixed_hz=fixed_hz)


@pytest.mark.parametrize("value", [True, 60.0, "60"])
def test_non_integer_fixed_hz_is_rejected(value: object) -> None:
    with pytest.raises(ConfigurationError, match="must be an integer"):
        EngineConfig(fixed_hz=cast(int, value))
