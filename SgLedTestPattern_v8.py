#! python3
# SgLedTestPattern_v1.py

# My first attempt at a LED test pattern generator.

# logging
import logging

logging.basicConfig(
    filename='LedTestPatternLog.txt',
    level=logging.DEBUG,
    format=' %(asctime)s - %(levelname)s - %(message)s'
)

# disables logging
# logging.disable(logging.CRITICAL)

# Import pillow image module
from PIL import Image, ImageDraw, ImageFont, ImageColor
import os

logging.debug(' Start of program')


# Function to validate resolution input
logging.debug('Start of resolution Validation function definition')


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
    logging.debug('resolution Validation function returning value')
    return value


''' Checks to  see if there is a row of half panels and 
    returns True if there is a row of half panels.
    Returns False if there is not a row of half panels.
    Also returns tile height number
'''


def half_tile_check(i):
    error1 = '\nThat is not a valid panel height\nEither use a whole number or add .5 for half panel\n'
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
        except IndexError:
            x = False
            i = TILECOUNT
            break
    return x, int(i)


# Function to validate the background color
logging.debug('Start of background color Validation definition')


def color_input_validation():
    while True:
        try:
            color = input('\n' + 'What is the background color of the tile? ')
            rgbCol = ImageColor.getcolor(str(color), 'RGBA')
        except ValueError:
            print('That is not a color I recognize, please try again. ')
            # better try again ... return to the start of the loop
            continue
        else:
            # input succesfully parsed!
            # ready to exit the loop.
            break
    logging.debug('color validation function returning value. ')
    logging.debug('color value (not returned to program): ' + str(color))
    return rgbCol


def even_is_true(i):
    i = int(i)
    if (i % 2) == 0:
        x = True
    else:
        x = False
    return x


# Ask for user input of LED tile dimensions and bg color
tileResWidth = int_input_validation(
    '\n' + 'What is the tile width (horizontal resolution)? '
)
tileResHeight = int_input_validation(
    '\n' + 'What is the tile height (vertical resolution)? '
)

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

''' Function to add a 1 pixel border
 likely need to call open image if sending an image to the function that
 is not already open
'''
def makeBorder(image):
    # border color
    borderColor = ImageColor.getcolor('white', 'RGBA')
    try:
        width, height = image.size
        # top and bottom borders
        logging.debug('Start drawing top and bottom borders')
        for x in range(width):
            for y in range(1):
                image.putpixel((x, y), borderColor)
            for y in range(height - 1, height):
                image.putpixel((x, y), borderColor)
        # left and right borders
        logging.debug('Start drawing left and right borders')
        for y in range(height):
            for x in range(1):
                image.putpixel((x, y), borderColor)
            for x in range(width - 1, width):
                image.putpixel((x, y), borderColor)
    except ValueError:
        print('There is a problem with the image called to the function')


# Create new image of LED panel color 1
logging.debug('Start of Create New Image ')
ledIm = Image.new('RGBA', (tileResWidth, tileResHeight), bgColor)

# Call make border function to add the border
makeBorder(ledIm)

# Create new image of LED panels color 2
logging.debug('lightens color by 50%')
r, g, b, a = bgColor
r = int(r * 0.7)
g = int(g * 0.7)
b = int(b * 0.7)
bgColor2 = r, g, b, a
logging.debug('Start for loop to copy panel images (second color) ' + str(bgColor2))

ledIm2 = Image.new('RGBA', (tileResWidth, tileResHeight), bgColor2)
logging.debug('size of ledIm2 is: ' + str(ledIm2.size))

# Call make border function to add the border to LED color panel 2
makeBorder(ledIm2)


# Ask for user input of wall dimensions
logging.debug('Start tiling panels onto wall pattern')
wallPanelWidth = int_input_validation(
    '\n' + 'How many tiles wide do you need the pattern? '
)
half_tile_bool, wallPanelHeight = half_tile_check(
    '\n' + 'How many tiles high do you need the pattern? (half-tiles are ok) '
)


if half_tile_bool == True:
    logging.debug('half tile is TRUE')
    ledIm3_half = Image.new('RGBA', (tileResWidth, int(tileResHeight / 2)), bgColor)
    ledIm4_half = Image.new('RGBA', (tileResWidth, int(tileResHeight / 2)), bgColor2)
    makeBorder(ledIm3_half)
    makeBorder(ledIm4_half)
else:
    logging.debug('half tile is false')


logging.debug('Program continues after half_tile_bool')

# Create new image at size of wall
if half_tile_bool == True:
    wallIm = Image.new(
        'RGBA',
        (
            wallPanelWidth * tileResWidth,
            (wallPanelHeight * tileResHeight) + int(tileResHeight / 2),
        ),
    )
else:
    wallIm = Image.new(
        'RGBA', (wallPanelWidth * tileResWidth, wallPanelHeight * tileResHeight)
    )

logging.debug('wallIm size = ' + str(wallIm.size))
logging.debug('wallPanelWidth 118 = ' + str(wallPanelWidth))
logging.debug('wallPanelHeight = ' + str(wallPanelHeight))
logging.debug('tileResWidth 119 = ' + str(tileResWidth))
logging.debug('tileResHeight 120 = ' + str(tileResHeight))

# For loop tiling LED panels onto wall image with alternating colors
wallPanelWidth2, wallPanelHeight2 = wallIm.size
tileResWidth, tileResHeight = ledIm.size

logging.debug('wallPanelWidth = ' + str(wallPanelWidth))
logging.debug('tileResWidth = ' + str(tileResWidth))
logging.debug('Start for loop to copy panel images with alternating colors')

logging.debug('wallPanelHeight begin loop at 213 = ' + str(wallPanelHeight))
logging.debug('wallPanelHeight = ' + str(wallPanelHeight2))

for left in range(0, wallPanelWidth2, tileResWidth * 2):
    for top in range(0, wallPanelHeight2, tileResHeight * 2):
        wallIm.paste(ledIm, (left, top))
for leftAlt in range(tileResWidth, wallPanelWidth2, tileResWidth * 2):
    for topAlt in range(tileResHeight, wallPanelHeight2, tileResHeight * 2):
        wallIm.paste(ledIm, (leftAlt, topAlt))
for left in range(0, wallPanelWidth2, tileResWidth * 2):
    for top in range(tileResHeight, wallPanelHeight2, tileResHeight * 2):
        wallIm.paste(ledIm2, (left, top))
for leftAlt in range(tileResWidth, wallPanelWidth2, tileResWidth * 2):
    for topAlt in range(0, wallPanelHeight2, tileResHeight * 2):
        wallIm.paste(ledIm2, (leftAlt, topAlt))

logging.debug('wallPanelHeight begin loop at 229 = ' + str(wallPanelHeight))
logging.debug('wallPanelHeight = ' + str(wallPanelHeight2))

# If half panels then do this - alternates half-panel colors
if half_tile_bool == True:
    if even_is_true(wallPanelHeight) == True:
        tile_color_1 = ledIm3_half
        tile_color_2 = ledIm4_half
    else:
        tile_color_1 = ledIm4_half
        tile_color_2 = ledIm3_half
    for left in range(0, wallPanelWidth2, tileResWidth * 2):
        for top in range(
            (wallPanelHeight2 - int(tileResHeight / 2)),
            wallPanelHeight2,
            int(tileResHeight / 2) * 2,
        ):
            wallIm.paste(tile_color_1, (left, top))
    for leftAlt in range(tileResWidth, wallPanelWidth2, tileResWidth * 2):
        for topAlt in range(
            (wallPanelHeight2 - (int(tileResHeight / 2))),
            wallPanelHeight2,
            tileResHeight * 2,
        ):
            wallIm.paste(tile_color_2, (leftAlt, topAlt))


logging.debug('For loop A copying led panels to wall complete')
logging.debug('tileResWidth 141 = ' + str(tileResWidth))
logging.debug('tileResHeight 142 = ' + str(tileResHeight))
logging.debug('wallPanelHeight = ' + str(wallPanelHeight))
logging.debug('wallPanelHeight = ' + str(wallPanelHeight2))


# creating variables to loop later - also centering the text
draw = ImageDraw.Draw(wallIm)
W, H, half_H = (tileResWidth, tileResHeight, (tileResHeight / 2))

logging.debug('W = ' + str(W) + 'H = ' + str(H) + 'half_H = ' + str(half_H))

# calculate appropriate font size for panel resolution
fontCal = int(min(tileResHeight, tileResWidth) / 2 * 0.6)
fontsFolder = 'FONT_FOLDER'
arialFont = ImageFont.truetype(os.path.join(fontsFolder, 'arial.ttf'), fontCal)

''' these variables are defined outside the loops
    so they can be manipulated
    List (needs to be converted to string for use)
'''
indexNums = [1, 1]

# This function converts list to string for use in draw.text lines
def iNc(i):
    i = ', '.join(str(e) for e in indexNums)
    return i


# calculates the width and height of text to be drawn
w, h = draw.textsize(iNc(indexNums), font=arialFont)

# centering text math constants
CENT_X_CORD_FOR_TEXT, CENT_Y_CORD_FOR_TEXT = (W - w) / 2, (H - h) / 2
adjusted_x_coord_for_text, adjusted_y_coord_for_text = (
    CENT_X_CORD_FOR_TEXT,
    CENT_Y_CORD_FOR_TEXT,
)
if half_tile_bool == True:
    CENT_half_Y_CORD_FOR_TEXT = (half_H - h) / 2
    adjusted_y_coord_for_text_halfpanel = CENT_half_Y_CORD_FOR_TEXT

# TODO: Deduplicate some of this code

# loop that draws text across tiles and counts up panel indexNums
while True:
    logging.debug('Start while true')
    loop_counter1 = 0

    # original while statement
    # while indexNums[0] <= wallPanelWidth + 1:

    while indexNums[0] <= wallPanelWidth:

        loop_counter1 += 1
        logging.debug(
            'While 1 statement start. ' + str(loop_counter1) + str(' ') + str(indexNums)
        )

        adjusted_x_coord_for_text = ((W - w) / 2) + (indexNums[0] - 1) * tileResWidth
        adjusted_y_coord_for_text = ((H - h) / 2) + (indexNums[1] - 1) * tileResHeight

        # adds more text to half panels if they exist
        if half_tile_bool == True:
            adjusted_x_coord_for_text_halfpanel = \
                ((W - w) / 2) + (indexNums[0] - 1) * tileResWidth
            adjusted_y_coord_for_text_halfpanel = \
                ((half_H - h) / 2) + (indexNums[1]) * (tileResHeight)

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

        logging.debug('indexNums update 370 ' +str(indexNums))

        # calculates the width and height of text to be drawn
        w, h = draw.textsize(iNc(indexNums), font=arialFont)

        # This if statements draws the half-tile numbers
        if half_tile_bool == True:
            logging.debug('Begin drawing half-tile text ')

            # TODO: Some way to only draw if tile is half width?
            if indexNums[1] == wallPanelHeight + 1:
                # draws text on the half panel
                draw.text(
                    (
                        adjusted_x_coord_for_text_halfpanel,
                        adjusted_y_coord_for_text_halfpanel,
                    ),
                    iNc(indexNums),
                    fill='gray',
                    font=arialFont,
                )
            logging.debug('END IF statement LOWER drawing half-tile text ' + str(indexNums))
            logging.debug('iNc function output = ' + str(iNc(indexNums)))
            logging.debug('adjusted_x_coord_for_text_halfpanel = ' + str(adjusted_x_coord_for_text_halfpanel))
            logging.debug('adjusted_y_coord_for_text_halfpanel = ' + str(adjusted_y_coord_for_text_halfpanel))
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
            logging.debug(
                'draw.textsize w value = ' + str(w) + '-- h value = ' + str(h)
            )

    break


# TODO: add information overlays (resolution, what else)

# TODO: combine multiple grids onto the same image

# TODO: add information to grid bg


logging.debug('wallPanelWidth value is: '
    + str(wallPanelWidth)
    + '\n END OF PROGRAM \n \n \n'
)

# test edit of festival pattern option git rep branch
# main branch should not have this edit

# saves image file
wallIm.save('wallTestGrid_1.png')
