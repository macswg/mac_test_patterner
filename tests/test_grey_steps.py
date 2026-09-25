"""Tests for src/greyStepsPatternMaker_v3.py."""
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import greyStepsPatternMaker_v3 as grey  # noqa: E402


@pytest.mark.parametrize('steps', [8, 12, 16, 24])
def test_grey_values_span_and_limits(steps):
    values = grey.grey_values(steps)
    assert len(values) == steps - 1
    assert values[0] == 0 and values[-1] == 255
    assert values == sorted(values)
    lowIndex = steps // 4 - 1
    assert values[lowIndex] == 16
    assert values[lowIndex + steps // 2] == 235


@pytest.mark.parametrize('steps', [6, 10, 13])
def test_grey_values_rejects_bad_steps(steps):
    with pytest.raises(ValueError):
        grey.grey_values(steps)


@pytest.mark.parametrize('size', [(1920, 1080), (3840, 2160), (5000, 1000), (1001, 777), (300, 900)])
def test_bars_fill_full_width(size):
    w, h = size
    im = grey.make_grey_steps(w, h)
    assert im.size == size
    values = grey.grey_values(grey.default_steps(w))
    edges = grey.bar_edges(w, len(values))
    # sample the bottom row (below any text) at each bar's center
    for i, value in enumerate(values):
        x = (edges[i] + edges[i + 1]) // 2
        assert im.getpixel((x, h - 1)) == (value, value, value)
    # last column is the final super-white bar, not a leftover gap
    assert im.getpixel((w - 1, h - 1)) == (255, 255, 255)

