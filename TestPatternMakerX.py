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

int_input_validation = raster_maker.int_input_validation
makeBorder = raster_maker.makeBorder
wLLsz = raster_maker.wLLsz

# This defines a variables that will be updated later
fontsFolder = 'FONT_FOLDER'

# Checks os and updates font name
if sys.platform.startswith('darwin'):
    fontName = 'Arial.ttf'
elif sys.platform.startswith('win'):
    fontName = 'arial.ttf'

pixelSpaceWidth = int_input_validation(
    '\n' + 'Enter the width of the pixel space: ')
pixelSpaceHeight = int_input_validation(
    '\n' + 'Enter the height of the pixel space: ')
pixelSpaceName = input('What is the pixelspace label? ')
bgBackgroundColor = ImageColor.getcolor('black', 'RGBA')  # Background color
bg = Image.new('RGBA', (pixelSpaceWidth, pixelSpaceHeight), bgBackgroundColor)

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
    
    """
    TEXT OVERLAY on FEST PATTERN -- These lines draw resolution and
    label of festival test pattern.
    """
    draw = ImageDraw.Draw(bg)
    draw.fontmode = 'L'
    xyOffsetTextSize = int(width * 0.03) 
    # fest_res_text = wLLsz(overlay.size)

    arialFont = ImageFont.truetype(os.path.join(fontsFolder, fontName), xyOffsetTextSize)

    # define vars for function that draws resolution text overlay
    # W, H, = scale_w, scale_h
    # w, h = getSizeOfText(fest_res_text, arialFont)
    # text_size = CalcCenter(W, H, w, h)
    # text_x, text_y = text_size
    # text_y = text_y + h
    # text_size = text_x, text_y

    # draws x, y offset text
    text = '(' + str(xOffset) + ', ' + str(yOffset) + ')'
    offsetText = ((xOffset + 1), yOffset)
    draw.text(offsetText, text, fill='white', font=arialFont)



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


