#! python3
# TestPatternMakerJSON.py


import logging
import raster_maker_json
from PIL import Image, ImageDraw, ImageFont, ImageColor
import os
import sys
import json

logging.basicConfig(
    filename='Log_TestPatternMakerJSON.txt',
    level=logging.DEBUG,
    format=' %(asctime)s - %(levelname)s - %(message)s',
)
# disables logging when uncommented
logging.disable(logging.CRITICAL)
logging.debug(' Start of program')


int_input_validation = raster_maker_json.int_input_validation
makeBorder = raster_maker_json.makeBorder
wLLsz = raster_maker_json.wLLsz
# getSizeOfText = raster_maker_json.getSizeOfText


def getSizeOfText(text, font):
    w, h = draw.textsize(text, font)
    return w, h


# This defines a variables that will be updated later
fontsFolder = 'FONT_FOLDER'

# Checks os and updates font name
if sys.platform.startswith('darwin'):
    fontName = 'Arial.ttf'
elif sys.platform.startswith('win'):
    fontName = 'arial.ttf'


#######
####### Import parameters from JSON
Jfile = r'./JSON_test_pattern_configs/TestPatterConfig1.json'
with open(Jfile, 'r', encoding='utf-8') as Jf:
    json_data = json.load(Jf)

# psJ = json_data[0][0]['pixelspace'] 

# pixelSpaceWidth = psJ['size'][0]
# pixelSpaceHeight = psJ['size'][1]
# pixelSpaceName = psJ['name']
# bgBackgroundColor = ImageColor.getcolor('black', 'RGBA')  # Background color
# bg = Image.new('RGBA', (pixelSpaceWidth, pixelSpaceHeight), bgBackgroundColor)
# b = makeBorder(bg)

### JSON data
rasterNum = 1  # starts at raster number 1
psNum = 0
rasterName = json_data[psNum][1][f'raster{rasterNum}']  # raster var to update for next raster


def addRaster(rasterName):
    xOffset = rasterName['x offset']
    yOffset = rasterName['y offset']
    # xOffset = int_input_validation(
    #     '\n' + 'What is the x offset of the raster from top left? ' +
    #     '\n' + f'Minimum offset to prevent overlap is {x, y} ')
    # yOffset = int_input_validation(
    #     '\n' + 'What is the y offset of the raster from top left? ')
    overlay = raster_maker_json.main(rasterName)
    bg.paste(overlay, (xOffset, yOffset))
    width, height = overlay.size
    
    """
    TEXT OVERLAY on FEST PATTERN -- These lines draw resolution and
    label of festival test pattern.
    """
    draw = ImageDraw.Draw(bg)
    draw.fontmode = 'L'
    xyOffsetTextSize = int(width * 0.023) 
    # fest_res_text = wLLsz(overlay.size)

    arialFont = ImageFont.truetype(os.path.join(fontsFolder, fontName), xyOffsetTextSize)

    # draws x, y offset text
    textTL = '(' + str(xOffset) + ', ' + str(yOffset) + ')'
    offsetTextxy = ((xOffset + 3), yOffset)
    draw.text(offsetTextxy, textTL, fill='white', font=arialFont)
    
    return bg, xyOffsetTextSize


for i in range(2):
    try:
        psJ = json_data[psNum][0]['pixelspace'] 
        pixelSpaceWidth = psJ['size'][0]
        pixelSpaceHeight = psJ['size'][1]
        pixelSpaceName = psJ['name']
        bgBackgroundColor = ImageColor.getcolor('black', 'RGBA')  # Background color
        bg = Image.new('RGBA', (pixelSpaceWidth, pixelSpaceHeight), bgBackgroundColor)
        b = makeBorder(bg)

        ### updating this while loop for JSON usage
        for i in json_data:
            for j in i[1]:
                bg, xyOffsetTextSize = addRaster(rasterName=rasterName)
                try:
                    rasterNum += 1
                    rasterName = json_data[psNum][1][f'raster{rasterNum}']  # raster var to update for next raster
                except KeyError:
                    break

        bgW, bgH = bg.size
        textBR = '(' + str(bgW) + ', ' + str(bgH) + ')'
        # xyOffsetTextSize = int(bgW * 0.023)
        arialFont = ImageFont.truetype(os.path.join(fontsFolder, fontName), xyOffsetTextSize)

        draw = ImageDraw.Draw(bg)
        draw.fontmode = 'L'
        bgTextW, bgTextH = getSizeOfText(textBR, arialFont)
        bgSizeTextxy = ((bgW - (bgTextW + int(bgTextW * 0.015))), (bgH - (bgTextH + int(bgTextW * 0.015))))
        draw.text(bgSizeTextxy, textBR, fill='white', font=arialFont)

        # saves image file
        imageDir = './images'
        fileName = f'{pixelSpaceName}.png'
        bg.save(os.path.join(imageDir, fileName))
        # bg.save(f'{pixelSpaceName}.png')
        psNum += 1
        rasterNum = 1
        rasterName = json_data[psNum][1][f'raster{rasterNum}']  # raster var to update for next raster
    except IndexError:
        break

