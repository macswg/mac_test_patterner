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
# logging.disable(logging.CRITICAL)
logging.debug(' Start of program')


# int_input_validation = raster_maker_json.int_input_validation
makeBorder = raster_maker_json.makeBorder
wLLsz = raster_maker_json.wLLsz


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


# ---- Import parameters from JSON
Jfile = r'./JSON_test_pattern_configs/TestPatterConfig1.json'
with open(Jfile, 'r', encoding='utf-8') as Jf:
    json_data = json.load(Jf)


# --- JSON data
rasterNum = 1  # starts at raster number 1
psNum = 0
rasterName = json_data[psNum][1][f'raster{rasterNum}']  # raster var to update for next raster


def cal_best_font_size(w, h):
    # area = int(w) * int(h)
    # # smaller_var = area / 16
    # new_size = area * 0.00015
    pass
    # return new_size


def addRaster(rasterName):
    xOffset = rasterName['x offset']
    yOffset = rasterName['y offset']
    overlay = raster_maker_json.make_raster(rasterName)
    bg.paste(overlay, (xOffset, yOffset))
    width, height = overlay.size

    """
    TEXT OVERLAY on FEST PATTERN -- These lines draw resolution and
    label of festival test pattern.
    """
    draw = ImageDraw.Draw(bg)
    draw.fontmode = 'L'
    # xyOffsetTextSize = int(width * 0.023)
    # print(width, height)
    # print(cal_best_font_size(width, height))
    xyOffsetTextSize = int(20)
    # fest_res_text = wLLsz(overlay.size)

    arialFont = ImageFont.truetype(os.path.join(fontsFolder, fontName), xyOffsetTextSize)

    # draws x, y offset text
    textTL = '(' + str(xOffset) + ', ' + str(yOffset) + ')'
    offsetTextxy = ((xOffset + 3), yOffset)
    draw.text(offsetTextxy, textTL, fill='white', font=arialFont)
    
    return bg, xyOffsetTextSize


# ------- main code block ------- #

if __name__ == "__main__":
    for i in json_data:
        try:
            psJ = json_data[psNum][0]['pixelspace'] 
            pixelSpaceWidth = psJ['size'][0]
            pixelSpaceHeight = psJ['size'][1]
            pixelSpaceName = psJ['name']
            bgBackgroundColor = ImageColor.getcolor('black', 'RGBA')  # Background color
            bg = Image.new('RGBA', (pixelSpaceWidth, pixelSpaceHeight), bgBackgroundColor)
            b = makeBorder(bg)

            # updating this while loop for JSON usage
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
