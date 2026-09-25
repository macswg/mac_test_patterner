#! python3
# greyStepsPatternMaker.py

# Test pattern generator for checking full vs limited (video) range.
#
# The pattern is a row of vertical grey bars:
#   0 .. 16      full-range "sub-black" steps
#   16 .. 235    limited-range steps (highlighted by the "Limited" band)
#   235 .. 255   full-range "super-white" steps
# If a display or pipeline is clipping to limited range, the outer bars
# will merge into a single black / single white block.

import argparse
import os
import sys

from PIL import Image, ImageDraw, ImageFont

LIMITED_LOW_VALUE = 16
LIMITED_HIGH_VALUE = 235
FULL_LOW_VALUE = 0
FULL_HIGH_VALUE = 255

# Heights of the title bands as a fraction of the image height
FULL_BAND_HEIGHT = 0.058
LIMITED_BAND_HEIGHT = 0.095
LIMITED_BAND_ALPHA = 220

# Checks os and picks a font, matching the other scripts in this repo
fontsFolder = 'FONT_FOLDER'
if sys.platform.startswith('darwin'):
    fontName = 'Arial.ttf'
elif sys.platform.startswith('win'):
    fontName = 'arial.ttf'
else:
    fontsFolder = '/usr/share/fonts/truetype/dejavu'
    fontName = 'DejaVuSans-Bold.ttf'


def load_font(size):
    try:
        return ImageFont.truetype(os.path.join(fontsFolder, fontName), size)
    except OSError:
        return ImageFont.load_default(size)


def default_steps(wall_width):
    """Grey step count scales with resolution: 12 up to HD, 16 up to UHD, 24 above."""
    if wall_width <= 1920:
        return 12
    if wall_width <= 3840:
        return 16
    return 24


def linear_steps(start, end, count):
    """count + 1 evenly spaced integer values from start to end inclusive."""
    return [round(start + (end - start) * i / count) for i in range(count + 1)]


def grey_values(steps):
    """
    Bar brightness values for a given step count (must be a multiple of 4, >= 8).

    steps / 4 - 1 steps are used for each outer (full-range only) section and
    steps / 2 steps for the limited section, giving steps - 1 bars in total.
    """
    if steps < 8 or steps % 4:
        raise ValueError('steps must be a multiple of 4 and at least 8')
    outer = steps // 4 - 1
    middle = steps // 2
    low = linear_steps(FULL_LOW_VALUE, LIMITED_LOW_VALUE, outer)
    mid = linear_steps(LIMITED_LOW_VALUE, LIMITED_HIGH_VALUE, middle)[1:-1]
    high = linear_steps(LIMITED_HIGH_VALUE, FULL_HIGH_VALUE, outer)
    return low + mid + high


def bar_edges(wall_width, bar_count):
    """x positions of bar edges; widths differ by at most 1px so bars fill the width exactly."""
    return [round(i * wall_width / bar_count) for i in range(bar_count + 1)]


def make_grey_steps(wall_width, wall_height, steps=None):
    """Build the grey steps pattern and return it as an RGB PIL Image."""
    if wall_width <= 0 or wall_height <= 0:
        raise ValueError('width and height must be positive')
    steps = steps or default_steps(wall_width)
    values = grey_values(steps)
    edges = bar_edges(wall_width, len(values))
    lowIndex = steps // 4 - 1
    highIndex = lowIndex + steps // 2

    greyIm = Image.new('RGBA', (wall_width, wall_height), (0, 0, 0, 255))
    draw = ImageDraw.Draw(greyIm)
    draw.fontmode = 'L'

    # grey bars
    for i, value in enumerate(values):
        draw.rectangle(
            (edges[i], 0, edges[i + 1] - 1, wall_height - 1),
            fill=(value, value, value, 255),
        )

    # title bands: solid black across the top, translucent black over the limited bars
    fullBandH = max(1, int(wall_height * FULL_BAND_HEIGHT))
    limBandH = max(1, int(wall_height * LIMITED_BAND_HEIGHT))
    limBandX0, limBandX1 = edges[lowIndex], edges[highIndex + 1]
    draw.rectangle((0, 0, wall_width - 1, fullBandH - 1), fill=(0, 0, 0, 255))
    limitedBand = Image.new(
        'RGBA', (limBandX1 - limBandX0, limBandH), (0, 0, 0, LIMITED_BAND_ALPHA)
    )
    greyIm.alpha_composite(limitedBand, (limBandX0, fullBandH))

    # font sized to the image, but never wider than a bar can hold
    minBarW = min(b - a for a, b in zip(edges, edges[1:]))
    fontSize = max(8, min(int(min(wall_width, wall_height) / 26), int(minBarW / 2.2)))
    font = load_font(fontSize)

    draw.text(
        (wall_width / 2, fullBandH / 2), 'Full Range',
        fill='white', font=font, anchor='mm',
    )
    draw.text(
        ((limBandX0 + limBandX1) / 2, fullBandH + limBandH * 0.7), 'Limited',
        fill='grey', font=font, anchor='mm',
    )

    # value label in each bar; dark text on the bright super-white bars
    labelY = fullBandH + limBandH * 0.25
    for i, value in enumerate(values):
        fillColor = 'black' if i > highIndex else 'grey'
        draw.text(
            ((edges[i] + edges[i + 1]) / 2, labelY), str(value),
            fill=fillColor, font=font, anchor='mm',
        )

    return greyIm.convert('RGB')


def int_input_validation(prompt):
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            value = 0
        if value > 0:
            return value
        print('You need to enter a positive integer (a whole number) ')


def main():
    parser = argparse.ArgumentParser(description='Make a full vs limited range grey steps test pattern.')
    parser.add_argument('width', nargs='?', type=int, help='horizontal resolution')
    parser.add_argument('height', nargs='?', type=int, help='vertical resolution')
    parser.add_argument('--steps', type=int, help='grey step count, a multiple of 4 (default scales with width)')
    args = parser.parse_args()

    wall_width = args.width or int_input_validation(
        '\n' + 'Enter the horizontal resolution of the test pattern: '
    )
    wall_height = args.height or int_input_validation(
        '\n' + 'Enter the vertical resolution of the test pattern: '
    )

    greyIm = make_grey_steps(wall_width, wall_height, args.steps)

    os.makedirs('images', exist_ok=True)
    outPath = os.path.join('images', f'greyTestPattern_{wall_width}x{wall_height}.png')
    greyIm.save(outPath)
    print(f'Saved {outPath}')


if __name__ == '__main__':
    main()
