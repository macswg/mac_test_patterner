# JSONScratch.py
# practicing JSON for python

import json
from PIL import ImageColor



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


##### example data format for fest pattern:
# rasterDict = {'raster1': {'x offset': 0,
#                        'y offset': 0,
#                        'festival pattern': True,
#                        'width': 1920,
#                        'height': 1080,
#                        'background color': 'darkviolet',
#                        'raster label': 'raster 1'}
#                         }

##### example data format for LED pattern:


file = r'./JSON_test_pattern_configs/TestPatterConfig1.json'

# Pixel Space 1 items
pixelspace = {'pixelspace': {'name': 'Lolla Argentina Sidescreens', 
                             'size': [3840, 2160]}}
rasterDict = {'raster1': {'x offset': 0,
                       'y offset': 0,
                       'festival pattern': True,
                       'width': 2990,
                       'height': 2160,
                       'background color': 'darkblue',
                       'raster label': 'Sidescreens'},
                       }
ps1 = [pixelspace, rasterDict]

# Pixel Space 2 items
pixelspace = {'pixelspace': {'name': 'Lolla Argentina USC', 
                             'size': [3840, 2160]}}
rasterDict = {'raster1': {'x offset': 0,
                       'y offset': 0,
                       'festival pattern': True,
                       'width': 2304,
                       'height': 1280,
                       'background color': 'darkgreen',
                       'raster label': 'USC'},
              'raster2': {'x offset': 0,
                       'y offset': 1290,
                       'festival pattern': True,
                       'width': 1536,
                       'height': 256,
                       'background color': 'darkviolet',
                       'raster label': 'USG'},
              'raster3': {'x offset': 1546,
                       'y offset': 1290,
                       'festival pattern': True,
                       'width': 720,
                       'height': 216,
                       'background color': 'darkviolet',
                       'raster label': 'DSW'},
                       }
ps2 = [pixelspace, rasterDict]


jsonData = [ps1, ps2]

# check jsonData for errors:
rasterNum = 1
colorsToCheck = jsonData[0][1]
for i in colorsToCheck:
    try:
        color_validation(colorsToCheck[f'raster{rasterNum}']['background color'])
        rasterNum += 1
    except KeyError:
        break

with open(file, 'w', encoding='utf-8') as f:
    json.dump(jsonData, f, indent=4)
