import pytest

from utils.cleaning.column_cleaner_lat_lng import _validate_lat_lng_boundary


@pytest.mark.parametrize(
    "coordinate",
    [
        (15.155854, 120.575012),
        (0.0, 0.0),
        (90.0, 180.0),
        (-90.0, -180.0),
        (90.0, -180.0),
        (-90.0, 180.0),
    ],
)
def test_preserves_valid_coordinates_including_boundaries(coordinate):
    assert _validate_lat_lng_boundary([coordinate]) == [coordinate]


@pytest.mark.parametrize(
    "coordinate",
    [
        (90.000001, 120.0),
        (-90.000001, 120.0),
        (15.0, 180.000001),
        (15.0, -180.000001),
        (float("inf"), 120.0),
        (float("-inf"), 120.0),
        (15.0, float("inf")),
        (15.0, float("-inf")),
        (float("nan"), 120.0),
        (15.0, float("nan")),
    ],
)
def test_replaces_out_of_range_or_non_finite_coordinates(coordinate):
    assert _validate_lat_lng_boundary([coordinate]) == [(None, None)]


@pytest.mark.parametrize(
    "coordinate",
    [(None, None), (None, 120.0), (15.0, None)],
)
def test_preserves_existing_missing_value_placeholders(coordinate):
    assert _validate_lat_lng_boundary([coordinate]) == [coordinate]


@pytest.mark.parametrize(
    "coordinate",
    [("15.0", 120.0), (15.0, "120.0"), (15, 120.0), (15.0, 120)],
)
def test_rejects_non_float_coordinates(coordinate):
    with pytest.raises(TypeError, match="lat or lng must be of float type"):
        _validate_lat_lng_boundary([coordinate])


def test_handles_empty_input():
    assert _validate_lat_lng_boundary([]) == []


def test_preserves_batch_order_and_does_not_mutate_input():
    coordinates = [(15.0, 120.0), (None, None), (-90.0, 180.0)]
    original = coordinates.copy()

    result = _validate_lat_lng_boundary(coordinates)

    assert result == original
    assert coordinates == original
    assert result is not coordinates
