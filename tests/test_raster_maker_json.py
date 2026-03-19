"""
Tests for raster_maker_json.make_raster.

Note: half-tile cases require mocking builtins.input because
raster_maker_json still prompts interactively for half-tile position.
"""
import pytest
from unittest.mock import patch
from PIL import Image
import raster_maker_json


def make_raster(overrides=None):
    base = {
        "festival pattern": False,
        "tile width": 48,
        "tile height": 48,
        "panels wide": 3,
        "panels high": 2,
        "half tile top": "n",
        "background color": "darkblue",
        "raster label": "test_raster",
        "width": 144,
        "height": 96,
        "x offset": 0,
        "y offset": 0,
    }
    if overrides:
        base.update(overrides)
    return raster_maker_json.make_raster(base)


# ── Basic raster ──────────────────────────────────────────────────────────────

def test_returns_image():
    assert isinstance(make_raster(), Image.Image)


def test_image_mode_is_rgba():
    assert make_raster().mode == "RGBA"


def test_basic_size():
    img = make_raster()
    assert img.size == (144, 96)


def test_white_border_corners():
    img = make_raster()
    w, h = img.size
    white = (255, 255, 255, 255)
    assert img.getpixel((0, 0)) == white
    assert img.getpixel((w - 1, 0)) == white
    assert img.getpixel((0, h - 1)) == white
    assert img.getpixel((w - 1, h - 1)) == white


def test_different_tile_sizes():
    img = make_raster({"tile width": 32, "tile height": 64, "panels wide": 4, "panels high": 3})
    assert img.size == (128, 192)


# ── Half-tile raster ──────────────────────────────────────────────────────────

def test_half_tile_bottom_size():
    # raster_maker_json prompts for half-tile position — mock input to pick bottom ("")
    with patch("builtins.input", return_value=""):
        img = make_raster({"panels high": "2.5"})
    assert img.size == (144, 120)


def test_half_tile_top_size():
    with patch("builtins.input", return_value="y"):
        img = make_raster({"panels high": "2.5"})
    assert img.size == (144, 120)


# ── Festival pattern ──────────────────────────────────────────────────────────

def test_festival_pattern_size():
    img = make_raster({
        "festival pattern": True,
        "width": 200,
        "height": 100,
        "background color": "black",
        "raster label": "fest_test",
    })
    assert img.size == (200, 100)


def test_festival_pattern_returns_image():
    img = make_raster({
        "festival pattern": True,
        "width": 160,
        "height": 90,
        "background color": "black",
        "raster label": "fest_test",
    })
    assert isinstance(img, Image.Image)


def test_festival_pattern_white_border():
    img = make_raster({
        "festival pattern": True,
        "width": 160,
        "height": 90,
        "background color": "black",
        "raster label": "fest_test",
    })
    w, h = img.size
    white = (255, 255, 255, 255)
    assert img.getpixel((0, 0)) == white
    assert img.getpixel((w - 1, h - 1)) == white
