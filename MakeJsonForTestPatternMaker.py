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


# ---- example data format for fest pattern:
# rasterDict = {'raster1': {'x offset': 0,
#                        'y offset': 0,
#                        'festival pattern': True,
#                        'width': 1920,
#                        'height': 1080,
#                        'background color': 'darkviolet',
#                        'raster label': 'raster 1'}
#                         }

# ---- example data format for LED pattern:


file = r'./JSON_test_pattern_configs/TestPatterConfig1.json'

# Pixel Space 1 items
pixelspace = {'pixelspace': {'name': 'TOP_content_raster_101', 
                             'size': [3840, 2160]}}
tileSize = {'tilesize': {'tilename': 'S9',
                         'tilewidth': 48,
                         'tileheight': 48}}
rasterDict = {'raster1': {'x offset': 2638,
                          'y offset': 10,
                          'festival pattern': False,
                          'width': 624,
                          'height': 768,
                          'tile width': 48,
                          'tile height': 48,
                          'panels wide': 13,
                          'panels high': 16,
                          'half tile top': 'n',
                          'background color': 'darkblue',
                          'raster label': 'Sidescreen SL'},
              'raster2': {'x offset': 10,
                          'y offset': 10,
                          'festival pattern': False,
                          'width': 624,
                          'height': 768,
                          'tile width': 48,
                          'tile height': 48,
                          'panels wide': 13,
                          'panels high': 16,
                          'half tile top': 'n',
                          'background color': 'darkred',
                          'raster label': 'Sidescreen SR'},
              'raster3': {'x offset': 2092,
                          'y offset': 10,
                          'festival pattern': False,
                          'width': 480,
                          'height': 768,
                          'tile width': 48,
                          'tile height': 48,
                          'panels wide': 10,
                          'panels high': 16,
                          'half tile top': 'n',
                          'background color': 'darkslateblue',
                          'raster label': 'USL'},
              'raster4': {'x offset': 1180,
                          'y offset': 10,
                          'festival pattern': False,
                          'width': 912,
                          'height': 768,
                          'tile width': 48,
                          'tile height': 48,
                          'panels wide': 19,
                          'panels high': 16,
                          'half tile top': 'n',
                          'background color': 'darkmagenta',
                          'raster label': 'USC'},
              'raster5': {'x offset': 700,
                          'y offset': 10,
                          'festival pattern': False,
                          'width': 480,
                          'height': 768,
                          'tile width': 48,
                          'tile height': 48,
                          'panels wide': 10,
                          'panels high': 16,
                          'half tile top': 'n',
                          'background color': 'maroon',
                          'raster label': 'USR'},
              'raster6': {'x offset': 10,
                          'y offset': 1180,
                          'festival pattern': False,
                          'width': 1920,
                          'height': 144,
                          'tile width': 48,
                          'tile height': 48,
                          'panels wide': 40,
                          'panels high': 3,
                          'half tile top': 'n',
                          'background color': 'darkgreen',
                          'raster label': 'riser'},
              'raster7': {'x offset': 10,
                          'y offset': 900,
                          'festival pattern': False,
                          'width': 768,
                          'height': 240,
                          'tile width': 48,
                          'tile height': 48,
                          'panels wide': 16,
                          'panels high': 5,
                          'half tile top': 'n',
                          'background color': 'darkred',
                          'raster label': 'flown SR'},
              'raster8': {'x offset': 1162,
                          'y offset': 900,
                          'festival pattern': False,
                          'width': 768,
                          'height': 240,
                          'tile width': 48,
                          'tile height': 48,
                          'panels wide': 16,
                          'panels high': 5,
                          'half tile top': 'n',
                          'background color': 'midnightblue',
                          'raster label': 'flown SL'},
              'raster9': {'x offset': 850,
                          'y offset': 900,
                          'festival pattern': True,
                          'width': 240,
                          'height': 240,
                          'tile width': 48,
                          'tile height': 48,
                          'panels wide': 18,
                          'panels high': 7,
                          'half tile top': 'n',
                          'background color': 'dimgray',
                          'raster label': 'LOGO'},
            # 'raster13': {'x offset': 1532,
            #               'y offset': 884,
            #               'festival pattern': True,
            #               'width': 432,
            #               'height': 288,
            #               'tile width': 48,
            #               'tile height': 48,
            #               'panels wide': 18,
            #               'panels high': 7,
            #               'half tile top': 'n',
            #               'background color': 'darkslateblue',
            #               'raster label': 'flown mid DSL'},
            #  'raster14': {'x offset': 2750,
            #               'y offset': 10,
            #               'festival pattern': True,
            #               'width': 1080,
            #               'height': 1920,
            #               'tile width': 48,
            #               'tile height': 48,
            #               'panels wide': 18,
            #               'panels high': 7,
            #               'half tile top': 'n',
            #               'background color': 'darkmagenta',
            #               'raster label': '220 IMAG'},
              }

ps1 = [pixelspace, rasterDict, tileSize]

# Pixel Space 2 items
pixelspace = {'pixelspace': {'name': 'Lolla Argentina USC', 
                             'size': [15360, 8640]}}
rasterDict = {'raster1': {'x offset': 10,
                          'y offset': 10,
                          'festival pattern': False,
                          'width': 240,
                          'height': 240,
                          'tile width': 72,
                          'tile height': 144,
                          'panels wide': 100,
                          'panels high': 50,
                          'half tile top': 'n',
                          'background color': 'dimgray',
                          'raster label': 'IGNORE USC'},
            #   'raster2': {'x offset': 720,
            #               'y offset': 10,
            #               'festival pattern': False,
            #               'width': 240,
            #               'height': 240,
            #               'tile width': 72,
            #               'tile height': 144,
            #               'panels wide': 3,
            #               'panels high': 7,
            #               'half tile top': 'n',
            #               'background color': 'dimgray',
            #               'raster label': 'IGNORE USC'},
              }
ps2 = [pixelspace, rasterDict, tileSize]

# Pixel Space 3 items
pixelspace = {'pixelspace': {'name': 'PS 3 USC', 
                             'size': [3840, 2160]}}
rasterDict = {'raster1': {'x offset': 0,
                          'y offset': 0,
                          'festival pattern': True,
                          'width': 2304,
                          'height': 1280,
                          'background color': 'orange',
                          'raster label': 'IGNORE PS3 raster'},
              }
ps3 = [pixelspace, rasterDict, tileSize]


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

with open(file, 'w', encoding='utf-8') as f:
    json.dump(jsonData, f, indent=4)
