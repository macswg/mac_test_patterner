#! python3
# TestPatternMakerX.py


import logging
import raster_maker
from PIL import Image, ImageDraw, ImageFont, ImageColor
import os
import sys

logging.basicConfig(
    filename='Log_TestPatternMakerX.txt',
    level=logging.DEBUG,
    format=' %(asctime)s - %(levelname)s - %(message)s',
)
# disables logging when uncommented
logging.disable(logging.CRITICAL)
logging.debug(' Start of program')

# TODO: Add background color option
# TODO: Add x,y overlay label to top corner
# TODO: Add raster 1 px border (not option in PGM but handy variable in script)

int_input_validation = raster_maker.int_input_validation
makeBorder = raster_maker.makeBorder

pixelSpaceWidth = int_input_validation(
    '\n' + 'Enter the width of the pixel space: ')
pixelSpaceHeight = int_input_validation(
    '\n' + 'Enter the height of the pixel space: ')
pixelSpaceName = input('What is the pixelspace label? ')
bg = Image.new('RGBA', (1920, 1080), (25, 25, 25))

b = makeBorder(bg)

def addRaster(x, y):
    xOffset = int_input_validation(
        '\n' + 'What is the x offset of the raster from top left? ' +
        '\n' + f'Minimum offset to prevent overlap is {x, y} ')
    yOffset = int_input_validation(
        '\n' + 'What is the y offset of the raster from top left? ')
    overlay = raster_maker.main()
    bg.paste(overlay, (xOffset, yOffset))
    width, height = overlay.size
    x += (width + xOffset)
    y += (height + yOffset)
    return bg, x, y


# bg = addRaster()
addRas = 'continue'
minX, minY = 0, 0

while True:
    bg, xOffset, yOffset = addRaster(minX, minY)
    addRas = input('Do you want to add another raster? y for yes; enter to quit.')
    minX += xOffset
    minY += yOffset
    if addRas == '':
        break


# raster1 = raster_maker.main()
# bg.paste(raster_maker.main(), (10, 10))

# overlay.paste(bg, (10, 10))

# saves image file
bg.save(f'{pixelSpaceName}.png')


