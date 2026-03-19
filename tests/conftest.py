import pytest
from unittest.mock import patch
from PIL import Image


@pytest.fixture(autouse=True)
def mock_image_save():
    """Prevent make_raster from writing PNG files to disk during tests."""
    with patch.object(Image.Image, "save"):
        yield
