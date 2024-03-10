# JSONScratch.py
# practicing JSON for python

import logging
import json
from PIL import ImageColor
import pandas as pd
import pygsheets
from typing import Dict, Any


# Logging info
logging.basicConfig(filename='ignore_LOG_makeJsonFromGoogle.md',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# disables logging up to a level specified when uncommented
# logging.disabled(logging.ERROR)
message = "\n \n *** START OF SCRIPT ***"
logging.info(message)


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
            # break
            return rgbCol


def g_sht_open(client: str, gSheet: str, wrksheet: str) -> pygsheets.Worksheet:
    """
    Opens the specified google sheet.
    """
    sht = client.open(gSheet)
    wks = sht.worksheet_by_title(wrksheet)
    return wks


def dataframe_to_dict(df: pd.DataFrame)


file = r'./JSON_test_pattern_configs/TestPtrnGoogleSheet_1.json'


# ------- Main Code Block -------
if __name__ == "__main__":
    client = pygsheets.authorize(
            service_file=(
                'secret/credentials_python-int-2023-2e89fbfc8ab6.json'))
    wks = g_sht_open(
        client=client, gSheet='Pixel Maps TOP 2024', wrksheet='ps1-contentmap')

    # import worksheet as pandas dataframe
    df = wks.get_as_df(start='A2')
    logging.info(f'DF row 1 = {df[1]}')

    


    ps1 = [pixelspace, rasterDict, tileSize]
    jsonData = [ps1]

    # check jsonData for errors:
    rasterNum = 1
    colorsToCheck = jsonData[0][1]
    for i in colorsToCheck:
        try:
            color_validation(colorsToCheck[f'raster{rasterNum}']['background color'])
            rasterNum += 1
        except KeyError:
            break

    # write jsonData to file
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(jsonData, f, indent=4)
