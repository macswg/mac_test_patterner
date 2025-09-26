#! python3
# TestPatternFromGoogleSheet.py

import logging
import raster_maker_google
# import json
from PIL import Image, ImageDraw, ImageFont, ImageColor
import os
import sys
import pandas as pd
import pygsheets
from typing import Dict, Any, List

# Logging info
logging.basicConfig(filename='ignore_LOG_makeJsonFromGoogle.md',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# disables logging up to a level specified when uncommented
# logging.disable(logging.ERROR)
message = "\n \n *** START OF SCRIPT ***"
logging.info(message)


# This defines a variables that will be updated later
fontsFolder = 'FONT_FOLDER'

# Checks os and updates font name
if sys.platform.startswith('darwin'):
    fontName = 'Arial.ttf'
elif sys.platform.startswith('win'):
    fontName = 'arial.ttf'

whiteBorderColor = ImageColor.getcolor('white', 'RGBA')
altBorderColor = ImageColor.getcolor('gray', 'RGBA')


def getSizeOfText(text, font):
    w, h = draw.textsize(text, font)
    return w, h


# Function to validate the background color
def color_validation(colorName):
    while True:
        try:
            color = colorName
            rgbCol = ImageColor.getcolor(str(color), 'RGBA')
        except ValueError:
            print(f'\'{colorName}\' is not a color I recognize, please try again. ')
            # better try again ... return to the start of the loop
            break
        else:
            # input succesfully parsed!
            # ready to exit the loop.
            return rgbCol


def makeBorder(image, color=whiteBorderColor):
    try:
        width, height = image.size
        for x in range(width):
            for y in range(1):
                image.putpixel((x, y), color)
            for y in range(height - 1, height):
                image.putpixel((x, y), color)
        for y in range(height):
            for x in range(1):
                image.putpixel((x, y), color)
            for x in range(width - 1, width):
                image.putpixel((x, y), color)
    except ValueError:
        print('There is a problem with the image called to the function')


# This function converts list to string for use in draw.text lines
def wLLsz(i):
    j = i
    i = ' x '.join(str(e) for e in j)
    return i


def g_sht_open(client: str, gSheet: str, wrksheet: str) -> pygsheets.Worksheet:
    """
    Opens the specified google sheet.
    """
    sht = client.open(gSheet)
    wks = sht.worksheet_by_title(wrksheet)
    return wks


# Function to convert DataFrame to list of dictionaries
def dataframe_to_list_of_dicts(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Convert each row of a pandas DataFrame into a dictionary, and collect them in a list.

    Args:
        df (pd.DataFrame): The DataFrame to convert.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, each representing a row from the DataFrame.
    """
    return df.to_dict('records')


def addRaster(rasterDict: Dict):
    xOffset = rasterDict['x offset']
    yOffset = rasterDict['y offset']
    overlay = raster_maker_google.make_raster(rasterDict=rasterDict)
    bg.paste(overlay, (xOffset, yOffset))
    width, height = overlay.size

    """
    TEXT OVERLAY on FEST PATTERN -- These lines draw resolution and
    label of festival test pattern.
    """
    draw = ImageDraw.Draw(bg)
    draw.fontmode = 'L'
    xyOffsetTextSize = int(20)

    arialFont = ImageFont.truetype(os.path.join(fontsFolder, fontName), xyOffsetTextSize)

    # draws x, y offset text
    textTL = '(' + str(xOffset) + ', ' + str(yOffset) + ')'
    offsetTextxy = ((xOffset + 3), yOffset)
    draw.text(offsetTextxy, textTL, fill='white', font=arialFont)

    return bg, xyOffsetTextSize


def column_to_list(df: pd.DataFrame, column_name: str) -> List:
    """Convert a specified column of a pandas DataFrame into a list.

    Args:
        df (pd.DataFrame): The pandas DataFrame containing the column.
        column_name (str): The name of the column to convert into a list.

    Returns:
        List: A list containing the values of the specified column.
    """
    # Ensure the column exists in the DataFrame
    if column_name in df.columns:
        return df[column_name].tolist()
    else:
        raise ValueError(f"Column '{column_name}' not found in DataFrame")


# ------- Main Code Block -------
if __name__ == "__main__":
    client = pygsheets.authorize(
            service_file=(
                'secret/credentials_python-int-2023-2e89fbfc8ab6.json'))
    
    g_sht_name = 'Sean - Pixel Maps iHeart Fiesta 2025'
    wks_rstr = g_sht_open(
        client=client, gSheet=g_sht_name, wrksheet='rasters')

    wks_ps = g_sht_open(
        client=client, gSheet=g_sht_name, wrksheet='pixelspaces')

    # import worksheet as pandas dataframe
    df = wks_rstr.get_as_df(start='A2')
    df_ps = wks_ps.get_as_df(start='A2')

    ps_list = column_to_list(df=df_ps, column_name='ps label')
    
    # Filter out empty strings and None values
    ps_list = [ps for ps in ps_list if ps and str(ps).strip()]

    # loop through filtered datasets
    for i in ps_list:
        rows_filt_ps = df[df['ps label'] == i]
        
        # Check if the filtered DataFrame is empty
        if rows_filt_ps.empty:
            print(f"Warning: No data found for ps label '{i}'. Skipping...")
            continue
            
        raster_dict_list = dataframe_to_list_of_dicts(rows_filt_ps)

        pixelSpaceWidth_row = rows_filt_ps['ps width']
        pixelSpaceWidth = pixelSpaceWidth_row.iloc[0]
        pixelSpaceHeight_row = rows_filt_ps['ps height']
        pixelSpaceHeight = pixelSpaceHeight_row.iloc[0]
        pixelSpaceName_row = rows_filt_ps['ps label']
        pixelSpaceName = pixelSpaceName_row.iloc[0]
        bgBackgroundColor = ImageColor.getcolor('black', 'RGBA')  # Background color
        bg = Image.new('RGBA', (pixelSpaceWidth, pixelSpaceHeight), bgBackgroundColor)
        # b = makeBorder(bg)
        for i in raster_dict_list:
            bg, xyOffsetTextSize = addRaster(i)

        bgW, bgH = bg.size
        textBR = '(' + str(bgW) + ', ' + str(bgH) + ')'
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

    # ------- output dict_list to JSON -------
    # jsonData = [dict_list]

    # # check jsonData for errors:
    # rasterNum = 1
    # colorsToCheck = jsonData[0][1]
    # for i in colorsToCheck:
    #     try:
    #         color_validation(colorsToCheck[f'raster{rasterNum}']['background color'])
    #         rasterNum += 1
    #     except KeyError:
    #         break

    # file = r'./JSON_test_pattern_configs/TestPtrnGoogleSheet_1.json'

    # # write jsonData to file
    # with open(file, 'w', encoding='utf-8') as f:
    #     json.dump(jsonData, f, indent=4)
    # -----------------------------------------
