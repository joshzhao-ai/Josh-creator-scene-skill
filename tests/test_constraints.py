import pytest

from creator_scene_director.constraints import assert_dual_coordinates


def test_dual_coordinate_guardrail() -> None:
    assert_dual_coordinates("主光位于画面右（人物左）前方 40°")
    with pytest.raises(ValueError, match="both frame-side"):
        assert_dual_coordinates("put the key on the left")

