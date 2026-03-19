"""
Tests for raster_maker_google.make_raster.

This module reads all config from a dict (no interactive prompts),
making it the cleanest target for unit testing.
"""
import pytest
from PIL import Image
import raster_maker_google


def make_raster(overrides=None):
    base = {
        "festival pattern": "FALSE",
        "tile width": 48,
        "tile height": 48,
        "panels wide": 3,
        "panels high": 2,
        "half tile top": "99",
        "background color": "darkblue",
        "raster label": "test_raster",
        "width": 144,
        "height": 96,
        "x offset": 0,
        "y offset": 0,
    }
    if overrides:
        base.update(overrides)
    return raster_maker_google.make_raster(base)


# ── Basic raster ──────────────────────────────────────────────────────────────

def test_returns_image():
    assert isinstance(make_raster(), Image.Image)


def test_image_mode_is_rgba():
    assert make_raster().mode == "RGBA"


def test_basic_size():
    # 3 tiles wide × 48px, 2 tiles high × 48px
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


def test_single_tile():
    img = make_raster({"tile width": 100, "tile height": 100, "panels wide": 1, "panels high": 1})
    assert img.size == (100, 100)


# ── Half-tile raster ──────────────────────────────────────────────────────────

def test_half_tile_bottom_size():
    # 2 full rows + 1 half row = 2×48 + 24 = 120
    img = make_raster({"panels high": 2.5, "half tile top": "99"})
    assert img.size == (144, 120)


def test_half_tile_top_size():
    img = make_raster({"panels high": 2.5, "half tile top": "0"})
    assert img.size == (144, 120)


def test_half_tile_middle_size():
    # half tile after row 1: same total height as bottom/top
    img = make_raster({"panels high": 2.5, "half tile top": "1"})
    assert img.size == (144, 120)


# ── Festival pattern ──────────────────────────────────────────────────────────

def test_festival_pattern_size():
    img = make_raster({
        "festival pattern": "TRUE",
        "width": 200,
        "height": 100,
        "background color": "black",
        "raster label": "fest_test",
    })
    assert img.size == (200, 100)


def test_festival_pattern_returns_image():
    img = make_raster({
        "festival pattern": "TRUE",
        "width": 160,
        "height": 90,
        "background color": "black",
        "raster label": "fest_test",
    })
    assert isinstance(img, Image.Image)


def test_festival_pattern_white_border():
    img = make_raster({
        "festival pattern": "TRUE",
        "width": 160,
        "height": 90,
        "background color": "black",
        "raster label": "fest_test",
    })
    w, h = img.size
    white = (255, 255, 255, 255)
    assert img.getpixel((0, 0)) == white
    assert img.getpixel((w - 1, h - 1)) == white
