#! python3
# SgLedTestPattern_v9.py

# My first attempt at a LED test pattern generator.

# logging
import logging
# Import pillow image module and other stuff
from PIL import Image, ImageDraw, ImageFont, ImageColor
import os
import sys


logging.basicConfig(
    filename='LedTestPatternLog.txt',
    level=logging.DEBUG,
    format=' %(asctime)s - %(levelname)s - %(message)s',
)
# disables logging when uncommented
logging.disable(logging.CRITICAL)
logging.debug(' Start of program')

#TODO: There is a bug here on the vertical offset that needs work.
# Variables to update to offset index numbers (1 is normal):
i_offset_0 = 1
i_offset_1 = 1


# Function to validate resolution input
def int_input_validation(prompt):
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print('You need to enter an non-negative integer (a whole number) ')
            # better try again ... return to the start of the loop
            continue
        else:
            # input successfully parsed!
            # we're ready to exit the loop.
            break
    return value


''' Checks to  see if there is a row of half panels and 
    returns True if there is a row of half panels.
    Returns False if there is not a row of half panels.
    Also returns tile height number
'''


def half_tile_check(i):
    error1 = (
        '\nThat is not a valid panel height\nEither use a whole number or add .5 for half panel\n'
    )
    while True:
        try:
            TILECOUNT = input(i)
            j = str(TILECOUNT).split('.')
            if j[1] == '5':
                x = True
                i = j[0]
                break
            elif int(j[1]) <= 4:
                print(error1)
                continue
            elif int(j[1]) >= 6:
                print(error1)
                continue
        except ValueError:
            print('Enter a whole number or a float value (i.e. x or x.5)')
            continue
        except IndexError:
            x = False
            i = TILECOUNT
            break
    return x, int(i)


# Function to validate the background color
def color_input_validation():
    while True:
        try:
            color = input('\n' + 'What is your background color? ')
            rgbCol = ImageColor.getcolor(str(color), 'RGBA')
        except ValueError:
            print('That is not a color I recognize, please try again. ')
            # better try again ... return to the start of the loop
            continue
        else:
            # input succesfully parsed!
            # ready to exit the loop.
            break
    logging.debug('color value = ' + str(color))
    return rgbCol


# Function to adjust every other panel to get the alternating grid colors.
def even_is_true(i):
    i = int(i)
    if (i % 2) == 0:
        x = True
    else:
        x = False
    return x


# This defines a variables that will be updated later
fontsFolder = 'FONT_FOLDER'

# Checks os and updates font name
if sys.platform.startswith('darwin'):
    fontName = 'Arial.ttf'
elif sys.platform.startswith('win'):
    fontName = 'arial.ttf'

# I'm making the fontCal variable a function:
# this line calculates the font size needed
# fontCal = int(min(tileResHeight, tileResWidth) / 2 * 0.6)


def fontCalFunc(i=72, j=72):
    x = int(min(i, j) / 2 * 0.6)
    return x


def getSizeOfText(text, font):
    w, h = draw.textsize(text, font)
    return w, h


# This function converts list to string for use in draw.text lines
def wLLsz(i):
    j = i
    i = ' x '.join(str(e) for e in j)
    return i


# W H = larger raster / w h = smaller raster to center
def CalcCenter(W, H, w, h):
    x = int(W / 2) - int(w / 2)
    y = int(H / 2) - int(h / 2)
    return x, y


''' Function to add a 1 pixel border
 likely need to call open image if sending an image to the function that
 is not already open.
 Border color defaults to white, but can add color argument.
'''

whiteBorderColor = ImageColor.getcolor('white', 'RGBA')
altBorderColor = ImageColor.getcolor('gray', 'RGBA')


def makeBorder(image, color=whiteBorderColor):
    # border color
    # borderColor = ImageColor.getcolor('white', 'RGBA')
    try:
        width, height = image.size
        # top and bottom borders
        logging.debug('Start drawing top and bottom borders')
        for x in range(width):
            for y in range(1):
                image.putpixel((x, y), color)
            for y in range(height - 1, height):
                image.putpixel((x, y), color)
        # left and right borders
        logging.debug('Start drawing left and right borders')
        for y in range(height):
            for x in range(1):
                image.putpixel((x, y), color)
            for x in range(width - 1, width):
                image.putpixel((x, y), color)
    except ValueError:
        print('There is a problem with the image called to the function')


# Function to return true if user selects half-panels to be on top of the raster
def half_tile_top_bool(i=False):
    i = input(
        '''\n Do you want to move the half-tiles to the top of the raster?
    [Type y for yes -- Leave blank to keep half-tiles at the bottom of the raster.] '''
    )
    if i == 'y':
        i = True
    else:
        i = False
    return i


# Festival input pattern
def fest_pattern_bool(i=False):
    i = input(
        '''Do you want to create a Festival Test Pattern with no LED outlines?
    [Type y for festival pattern -- Leave blank to draw LED panel outlines.] '''
    )
    if i == 'y':
        i = True
    else:
        i = False
    return i


fest_pattern = fest_pattern_bool()


# FESTIVAL TEST PATTERN -- IF SECTION

if fest_pattern is True:
    fest_wall_width = int_input_validation(
        '\n' + 'Enter the horizontal resolution of the test pattern: '
    )
    fest_wall_height = int_input_validation(
        '\n' + 'Enter the vertical resolution of the test pattern: '
    )
    fest_bgColor = color_input_validation()

    overlay_color = 127, 127, 127

    # create new image
    festIm = Image.new('RGBA', (fest_wall_width, fest_wall_height), fest_bgColor)

    fest_wallsize = festIm.size

    # Draw and scale an ellipse to remove anti-aliasing
    scale_factor = 4
    line_width = 10
    scale_w, scale_h = (
        (fest_wall_width * scale_factor),
        (fest_wall_height * scale_factor),
    )

# noqa: E302
    # PIL code: Create new image for circle and lines
    festOverlaysIm = Image.new('RGBA', (scale_w, scale_h), fest_bgColor)

    # Draw perfect circle
    drawFestPatterns = ImageDraw.Draw(festOverlaysIm)
    circRadius = min(scale_w, scale_h)
    circRadius_w_Pad = circRadius - (circRadius * 0.05)

    # create variables to draw a centered circle
    def circleCenterPoints(i=circRadius_w_Pad, j=scale_w, k=scale_h):
        tl_x = (j / 2) - (i / 2)
        tl_y = (k / 2) - (i / 2)
        br_x = (j / 2) + (i / 2)
        br_y = (k / 2) + (i / 2)
        return tl_x, tl_y, br_x, br_y

    drawFestPatterns.ellipse(
        circleCenterPoints(), 
        fill=None, outline=(overlay_color),
        width=line_width
    )

    # draw x lines
    drawFestPatterns.line((0, 0, scale_w, scale_h), fill='gray', width=line_width, joint=None)
    drawFestPatterns.line((0, scale_h, scale_w, 0), fill='gray', width=line_width, joint=None)

    # TEXT OVERLAY on FEST PATTERN -- These lines draw resolution and label of festival test pattern.
    draw = ImageDraw.Draw(festOverlaysIm)
    draw.fontmode = 'L'
    fest_res_text = wLLsz(fest_wallsize)

    # Asks user to enter a label
    fest_wall_label_text = input('What label do you want? ')
    if fest_wall_label_text == '':
        fest_wall_label_text = 'fest_test_pattern'

    # updates arialFont size
    font_scale_w, font_scale_h = scale_w / 4, scale_h / 4
    # makes text bigger if wall is smaller than 300 pixels
    if min(fest_wallsize) <= 300:
        font_scale_w, font_scale_h = scale_w / 2, scale_h / 2
    arialFont = ImageFont.truetype(
        os.path.join(fontsFolder, fontName), fontCalFunc(font_scale_w, font_scale_h)
    )
    
    # define vars for function that draws resolution text overlay
    W, H, = scale_w, scale_h
    w, h = getSizeOfText(fest_res_text, arialFont)
    text_size = CalcCenter(W, H, w, h)
    text_x, text_y = text_size
    text_y = text_y + h
    text_size = text_x, text_y

    # draws fest res text
    draw.text(
        text_size, fest_res_text, fill='white', font=arialFont,
    )

    # updates arialFont size for title overlay text
    font_scale_w, font_scale_h = scale_w / 4.5, scale_h / 4.5
    if min(fest_wallsize) <= 300:
        font_scale_w, font_scale_h = scale_w / 2, scale_h / 2
    arialTitleFont = ImageFont.truetype(
        os.path.join(fontsFolder, fontName), fontCalFunc(font_scale_w, font_scale_h)
    )

    # updates variables to adjust position of fest title screen text
    w, h = getSizeOfText(fest_wall_label_text, arialTitleFont)
    text_size = CalcCenter(W, H, w, h)
    text_x, text_y = text_size
    text_y = text_y - h  # moves text up
    text_size = text_x, text_y

    # draws fest wall label text
    draw.text(
        text_size, fest_wall_label_text, fill='white', font=arialTitleFont,
    )

    # scales festival overlays image to festival image size
    original_size = (fest_wall_width, fest_wall_height)
    festOverlaysIm = festOverlaysIm.resize(original_size, resample=1)

    # pastes scaled circle onto image
    festIm.paste(festOverlaysIm, (0, 0))

    # Call make border function to add the border
    makeBorder(festIm)

    # saves image file
    festIm.save(f'{fest_wall_label_text}.png')

    # exit program if fest pattern is true
    exit()


# Ask for user input of LED tile dimensions and bg color
tileResWidth = int_input_validation('\n' + 'What is the tile width (horizontal resolution)? ')
tileResHeight = int_input_validation('\n' + 'What is the tile height (vertical resolution)? ')

''' color is asked for in the color_input_validation function because
    I don't know how else to verify value is correct
'''
bgColor = color_input_validation()

# Log prints out summary of values captured for debugging's sake.
logging.debug(
    '\n' + 'Values returned to the program: ' + '\n'
    'tileResWidth is ' + str(tileResWidth) + '\n'
    'tileResHeight is ' + str(tileResHeight) + '\n'
    'color value is ' + str(bgColor) + '\n'
)

# Create new image of LED panel color 1
logging.debug('Start of Create New Image ')
ledIm = Image.new('RGBA', (tileResWidth, tileResHeight), bgColor)

# Call make border function to add the border
makeBorder(ledIm, altBorderColor)

# Create new image of LED panels color 2
logging.debug('lightens color by some percentage')
r, g, b, a = bgColor
r = int(r * 0.7)
g = int(g * 0.7)
b = int(b * 0.7)
bgColor2 = r, g, b, a

logging.debug('Start for loop to copy panel images (second color) ' + str(bgColor2))

ledIm2 = Image.new('RGBA', (tileResWidth, tileResHeight), bgColor2)
logging.debug('size of ledIm2 is: ' + str(ledIm2.size))

# Call make border function to add the border to LED color panel 2
makeBorder(ledIm2, altBorderColor)


# Ask for user input of wall dimensions
logging.debug('Start tiling panels onto wall pattern')
wallPanelWidth = int_input_validation('\n' + 'How many tiles wide do you need the pattern? ')
half_tile_bool, wallPanelHeight = half_tile_check(
    '\n' + 'How many tiles high do you need the pattern? (half-tiles are ok) '
)


if half_tile_bool is True:
    logging.debug('half tile is TRUE')
    ledIm3_half = Image.new('RGBA', (tileResWidth, int(tileResHeight / 2)), bgColor)
    ledIm4_half = Image.new('RGBA', (tileResWidth, int(tileResHeight / 2)), bgColor2)
    makeBorder(ledIm3_half, altBorderColor)
    makeBorder(ledIm4_half, altBorderColor)
    # Asks user if they want half-tiles on the top of the raster (leave blank for bottom)
    half_tile_top = half_tile_top_bool()
else:
    logging.debug('half tile is false')


logging.debug('Program continues after half_tile_bool')

# Create new image at size of wall
if half_tile_bool is True:
    wallIm = Image.new(
        'RGBA',
        (
            wallPanelWidth * tileResWidth,
            (wallPanelHeight * tileResHeight) + int(tileResHeight / 2),
        ),
    )
else:
    wallIm = Image.new('RGBA', (wallPanelWidth * tileResWidth, wallPanelHeight * tileResHeight))

logging.debug('wallIm size = ' + str(wallIm.size))
logging.debug('wallPanelWidth = ' + str(wallPanelWidth))
logging.debug('wallPanelHeight = ' + str(wallPanelHeight))
logging.debug('tileResWidth = ' + str(tileResWidth))
logging.debug('tileResHeight = ' + str(tileResHeight))

# noqa: E302


# FOR LOOP DRAWING LED PANELS onto wall image with alternating colors

wallPanelWidth2, wallPanelHeight2 = wallIm.size
tileResWidth, tileResHeight = ledIm.size

logging.debug('wallPanelWidth = ' + str(wallPanelWidth))
logging.debug('tileResWidth = ' + str(tileResWidth))
logging.debug('Start for loop to copy panel images with alternating colors')
logging.debug('wallPanelHeight begin loop at 213 = ' + str(wallPanelHeight))
logging.debug('wallPanelHeight = ' + str(wallPanelHeight2))


# Variables defined to start drawing full-panels at the top of the wall:
top_start = 0
top_start_alt = tileResHeight

logging.debug('\n' + 'top_start variable defined' + str(top_start) + str(top_start_alt))

# Updates start of tile loops by updating top start variables:
if half_tile_bool is True:
    if half_tile_top is True:
        top_start = 0 - wallPanelHeight2
        top_start_alt = tileResHeight - wallPanelHeight2

logging.debug('\n' + 'top_start variable defined again' + str(top_start) + str(top_start_alt) + '\n')

for left in range(0, wallPanelWidth2, tileResWidth * 2):
    for top in range(top_start, wallPanelHeight2, tileResHeight * 2):
        wallIm.paste(ledIm, (left, top))
for leftAlt in range(tileResWidth, wallPanelWidth2, tileResWidth * 2):
    for topAlt in range(top_start_alt, wallPanelHeight2, tileResHeight * 2):
        wallIm.paste(ledIm, (leftAlt, topAlt))
for left in range(0, wallPanelWidth2, tileResWidth * 2):
    for top in range(top_start_alt, wallPanelHeight2, tileResHeight * 2):
        wallIm.paste(ledIm2, (left, top))
for leftAlt in range(tileResWidth, wallPanelWidth2, tileResWidth * 2):
    for topAlt in range(top_start, wallPanelHeight2, tileResHeight * 2):
        wallIm.paste(ledIm2, (leftAlt, topAlt))

logging.debug('wallPanelHeight begin loop at 431 = ' + str(wallPanelHeight))
logging.debug('wallPanelHeight = ' + str(wallPanelHeight2))


#
#
# HALF PANELS -- Draws half-panels onto the wall image and alternates half-panel colors

if half_tile_bool is True:

    # If half-tiles on the top, this (and the following if statement) changes where half-tiles are drawn
    
    # default condition -- half-tile on bottom
    true_toggle = True
    top_start_half_panel = wallPanelHeight2 - (int(tileResHeight / 2))

logging.debug('For loop A copying led panels to wall complete')
logging.debug('tileResWidth 141 = ' + str(tileResWidth))
logging.debug('tileResHeight 142 = ' + str(tileResHeight))
logging.debug('wallPanelHeight = ' + str(wallPanelHeight))
logging.debug('wallPanelHeight = ' + str(wallPanelHeight2))


# creating variables to loop later - also centering the text
draw = ImageDraw.Draw(wallIm)
draw.fontmode = 'L'
W, H, half_H = (tileResWidth, tileResHeight, (tileResHeight / 2))

logging.debug('W = ' + str(W) + 'H = ' + str(H) + 'half_H = ' + str(half_H))

# calculate appropriate font size for panel resolution
fontCal = int(min(tileResHeight, tileResWidth) / 2 * 0.6)
arialFont = ImageFont.truetype(os.path.join(fontsFolder, fontName), fontCal)

''' these variables are defined outside the loops
    so they can be manipulated
    List (needs to be converted to string for use)
'''

indexNums = [i_offset_0, i_offset_1]

# This function converts list to string for use in draw.text lines


def iNc(i):
    i = ', '.join(str(e) for e in indexNums)
    return i


''' calculates the width and height of text to be drawn
    function below added later -- can eventually replace
    '# original line that calculates' line but rest of code 
    will need to be updated.
'''


# original line that calculates the width and height of text to be drawn
w, h = draw.textsize(iNc(indexNums), font=arialFont)

# centering text math constants
CENT_X_CORD_FOR_TEXT, CENT_Y_CORD_FOR_TEXT = (W - w) / 2, (H - h) / 2
adjusted_x_coord_for_text, adjusted_y_coord_for_text = (
    CENT_X_CORD_FOR_TEXT,
    CENT_Y_CORD_FOR_TEXT,
)
if half_tile_bool is True:
    CENT_half_Y_CORD_FOR_TEXT = (half_H - h) / 2
    adjusted_y_coord_for_text_halfpanel = CENT_half_Y_CORD_FOR_TEXT

# TODO: Deduplicate some of this code

# loop that draws text across tiles and counts up panel indexNums
while True:
    logging.debug('Start while true')
    loop_counter1 = 0

    # original while statement
    # while indexNums[0] <= wallPanelWidth + 1:

    while indexNums[0] <= wallPanelWidth + i_offset_0:

        loop_counter1 += 1

        logging.debug('While 1 statement start. ' + str(loop_counter1) + str(' ') + str(indexNums))

        adjusted_x_coord_for_text = ((W - w) / 2) + (indexNums[0] - i_offset_0) * tileResWidth
        adjusted_y_coord_for_text = ((H - h) / 2) + (indexNums[1] - i_offset_1) * tileResHeight
        # this if statement adjust the y variable above to move text up
        if half_tile_bool is True:
            if half_tile_top is True:
                adjusted_y_coord_for_text -= tileResHeight / 4
                if indexNums[1] >= 2:
                    adjusted_y_coord_for_text -= tileResHeight / 4
        # adds more text to half panels if they exist
        if half_tile_bool is True:
            adjusted_x_coord_for_text_halfpanel = ((W - w) / 2) + (indexNums[0] - i_offset_0) * tileResWidth
            adjusted_y_coord_for_text_halfpanel = ((half_H - h) / 2) + (indexNums[1]) * (
                tileResHeight
            )

        # calculates the width and height of text to be drawn
        w, h = draw.textsize(iNc(indexNums), font=arialFont)

        # draws text
        draw.text(
            (adjusted_x_coord_for_text, adjusted_y_coord_for_text),
            iNc(indexNums),
            fill='gray',
            font=arialFont,
        )

        # adds to index number
        indexNums[1] += 1

        logging.debug('indexNums update 370 ' + str(indexNums))

        # calculates the width and height of text to be drawn
        w, h = draw.textsize(iNc(indexNums), font=arialFont)

        # This if statements draws the half-tile numbers
        if half_tile_bool is True:
            logging.debug('Begin drawing half-tile text ')

            # TODO: Some way to only draw if tile is half width?
            if indexNums[1] == wallPanelHeight + 1:
                if half_tile_top is True:
                    adjusted_y_coord_for_text_halfpanel -= tileResHeight / 4
                # draws text on the half panel
                draw.text(
                    (adjusted_x_coord_for_text_halfpanel, adjusted_y_coord_for_text_halfpanel,),
                    iNc(indexNums),
                    fill='gray',
                    font=arialFont,
                )
            logging.debug('END IF statement LOWER drawing half-tile text ' + str(indexNums))
            logging.debug('iNc function output = ' + str(iNc(indexNums)))
            logging.debug(
                'adjusted_x_coord_for_text_halfpanel = ' + str(adjusted_x_coord_for_text_halfpanel)
            )
            logging.debug(
                'adjusted_y_coord_for_text_halfpanel = ' + str(adjusted_y_coord_for_text_halfpanel)
            )
            logging.debug('adjusted_x_coord_for_text = ' + str(adjusted_x_coord_for_text))
            logging.debug('adjusted_y_coord_for_text = ' + str(adjusted_y_coord_for_text) + '\n')

        # original if statement
        if indexNums[1] == wallPanelHeight + 1:
            logging.debug('Start if indexNums A. ' + str(indexNums))

            # these are necessary to prevent infinite loop
            indexNums[0] += 1
            indexNums[1] = 1

            adjusted_x_coord_for_text = CENT_X_CORD_FOR_TEXT
            adjusted_y_coord_for_text += tileResHeight

            # calculates the width and height of text to be drawn
            w, h = draw.textsize(iNc(indexNums), font=arialFont)
            logging.debug('draw.textsize w value = ' + str(w) + '-- h value = ' + str(h))

    break


# draw white border around entire test pattern
makeBorder(wallIm)


#
#
# INFORMATION OVERLAYS ON LED TEST PATTERN SECTION -- draws resolution and title overlays

wallsize = wallIm.size
wallsizeX, wallsizeY = wallIm.size

statsFontSize = fontCalFunc(wallsizeX / 4, wallsizeY / 4)
if min(wallsize) <= 300:
    statsFontSize = fontCalFunc(wallsizeX / 1.5, wallsizeY / 1.5)
arialFontStats = ImageFont.truetype(os.path.join(fontsFolder, fontName), statsFontSize)


# asks user for wall label
LED_wall_label_text = input('\n What label do you want on the raster? ')
if LED_wall_label_text == '':
    LED_wall_label_text = 'led_test_pattern'


# updates variables for image resolution text overlays
W, H, = wallsizeX, wallsizeY
w, h = getSizeOfText(wLLsz(wallsize), arialFontStats)
text_size = CalcCenter(W, H, w, h)
text_x, text_y = text_size
text_y = text_y + (h / 2)
text_size = text_x, text_y

# updates arialFont size for title overlay text
statsFontSize = fontCalFunc(wallsizeX / 4.5, wallsizeY / 4.5)
if min(wallsize) <= 300:
    statsFontSize = fontCalFunc(wallsizeX / 2, wallsizeY / 2)
arialTitleFont_LED = ImageFont.truetype(
    os.path.join(fontsFolder, fontName), statsFontSize
)

# draws stats text
draw.text(
    text_size, wLLsz(wallsize), fill='white', font=arialFontStats,
)


# updates variables for title overlays
w, h = getSizeOfText(LED_wall_label_text, arialTitleFont_LED)
text_size = CalcCenter(W, H, w, h)
text_x, text_y = text_size
text_y = text_y - h  # moves the text up
text_size = text_x, text_y

# draws Label text
draw.text(text_size, LED_wall_label_text, fill='white', font=arialTitleFont_LED)


# TODO: combine multiple grids onto the same image


# saves image file
wallIm.save(f'{LED_wall_label_text}.png')


logging.debug('wallPanelWidth value is: ' + str(wallPanelWidth) + '\n END OF PROGRAM \n \n \n')
