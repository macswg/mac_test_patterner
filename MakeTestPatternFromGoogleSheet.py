import logging
import raster_maker_google
import json
from PIL import ImageColor
import pandas as pd
import pygsheets
from typing import Dict, Any, List


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


file = r'./JSON_test_pattern_configs/TestPtrnGoogleSheet_1.json'


# ------- Main Code Block -------
if __name__ == "__main__":
    client = pygsheets.authorize(
            service_file=(
                'secret/credentials_python-int-2023-2e89fbfc8ab6.json'))
    wks = g_sht_open(
        client=client, gSheet='Pixel Maps TOP 2024', wrksheet='rasters')

    # import worksheet as pandas dataframe
    df = wks.get_as_df(start='A2')
    logging.info(f'DF row 1 = {df}')

    dict_list = dataframe_to_list_of_dicts(df)
    for d in dict_list:
        logging.info(f'dict_list = {d}')



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

    # # write jsonData to file
    # with open(file, 'w', encoding='utf-8') as f:
    #     json.dump(jsonData, f, indent=4)
    # -----------------------------------------
