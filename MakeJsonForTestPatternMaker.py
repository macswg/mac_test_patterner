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
pixelspace = {'pixelspace': {'name': 'pixel space one', 
                             'size': [3840, 2160]}}
rasterDict = {'raster1': {'x offset': 0,
                       'y offset': 0,
                       'festival pattern': True,
                       'width': 1920,
                       'height': 1080,
                       'background color': 'darkviolet',
                       'raster label': 'raster 1'},
              'raster2': {'x offset': 1920,
                       'y offset': 1080,
                       'festival pattern': True,
                       'width': 1920,
                       'height': 1080,
                       'background color': 'darkviolet',
                       'raster label': 'raster 2'},
              'raster3': {'x offset': 0,
                       'y offset': 1080,
                       'festival pattern': True,
                       'width': 1920,
                       'height': 1080,
                       'background color': 'darkgreen',
                       'raster label': 'raster 3'},
              'raster4': {'x offset': 1920,
                       'y offset': 0,
                       'festival pattern': True,
                       'width': 1920,
                       'height': 1080,
                       'background color': 'black',
                       'raster label': 'raster 4 black'}
                       }
ps1 = [pixelspace, rasterDict]


pixelspace = {'pixelspace': {'name': 'pixel space two', 
                             'size': [3840, 2160]}}
rasterDict = {'raster1': {'x offset': 0,
                       'y offset': 0,
                       'festival pattern': True,
                       'width': 1920,
                       'height': 1080,
                       'background color': 'darkviolet',
                       'raster label': 'raster 1'},
              'raster2': {'x offset': 1920,
                       'y offset': 1080,
                       'festival pattern': True,
                       'width': 1920,
                       'height': 1080,
                       'background color': 'darkviolet',
                       'raster label': 'raster 2'},
              'raster3': {'x offset': 0,
                       'y offset': 1080,
                       'festival pattern': True,
                       'width': 1920,
                       'height': 1080,
                       'background color': 'darkgreen',
                       'raster label': 'raster 3'},
              'raster4': {'x offset': 1920,
                       'y offset': 0,
                       'festival pattern': True,
                       'width': 1920,
                       'height': 1080,
                       'background color': 'black',
                       'raster label': 'raster 4 black'}
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
