#! python3
# raster_maker.py

""" makes test pattern rasters -- Call this from TestPatternMakerX.py to place
rasters inside a pixelspace (e.g. 1920x1080).
"""

# logging
# import logging
# Import pillow image module and other stuff
from PIL import Image, ImageDraw, ImageFont, ImageColor
import os
import sys
# import json

# logging.basicConfig(
#     filename='LedTestPatternLog.txt',
#     level=logging.DEBUG,
#     format=' %(asctime)s - %(levelname)s - %(message)s',
# )
# disables logging when uncommented
# logging.disable(logging.CRITICAL)
# logging.debug(' Start of program')

whiteBorderColor = ImageColor.getcolor('white', 'RGBA')
altBorderColor = ImageColor.getcolor('gray', 'RGBA')

imageDir = './images'

# ---- Import parameters from JSON
# Jfile = r'./JSON_test_pattern_configs/TestPatterConfig1.json'
# with open(Jfile, 'r', encoding='utf-8') as Jf:
#     json_data = json.load(Jf)

# festBoolJson = json_data[0][1]['raster1']['festival pattern']


# Function to validate resolution input
def int_validation(x: int):
    while True:
        try:
            value = int(x)
        except ValueError:
            print('You need to enter an non-negative integer (a whole number) ')
            # better try again ... return to the start of the loop
            continue
        else:
            # input successfully parsed!
            # we're ready to exit the loop.
            break
    return value


# def int_input_validation(prompt):
#     while True:
#         try:
#             value = int(prompt)
#         except ValueError:
#             print('You need to enter an non-negative integer (a whole number) ')
#             # better try again ... return to the start of the loop
#             continue
#         else:
#             # input successfully parsed!
#             # we're ready to exit the loop.
#             break
#     return value


# Function to validate the background color
def color_validation(colorName):
    while True:
        try:
            color = colorName
            rgbCol = ImageColor.getcolor(str(color), 'RGBA')
        except ValueError:
            print('That is not a color I recognize, please try again. ')
            # better try again ... return to the start of the loop
            continue
        else:
            # input succesfully parsed!
            # ready to exit the loop.
            break
    # logging.debug('color value = ' + str(color))
    return rgbCol


def makeBorder(image, color=whiteBorderColor):
    # border color
    # borderColor = ImageColor.getcolor('white', 'RGBA')
    try:
        width, height = image.size
        # top and bottom borders
        # logging.debug('Start drawing top and bottom borders')
        for x in range(width):
            for y in range(1):
                image.putpixel((x, y), color)
            for y in range(height - 1, height):
                image.putpixel((x, y), color)
        # left and right borders
        # logging.debug('Start drawing left and right borders')
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


def fontCalFunc(i=72, j=72):
    x = int(min(i, j) / 2 * 0.6)
    return x

# def getSizeOfText(text, font):
#     w, h = draw.textsize(text, font)
#     return w, h


def make_raster(rasterDict: dict):
    # TODO: There is a bug here on the vertical offset that needs work.
    # Variables to update to offset index numbers (1 is normal):
    i_offset_0 = 1
    i_offset_1 = 1

    """ Checks to  see if there is a row of half panels and 
        returns True if there is a row of half panels.
        Returns False if there is not a row of half panels.
        Also returns tile height number
    """

    def half_tile_check(i):
        error1 = (
            '''\nThat is not a valid panel height\nEither use a whole 
            number or add .5 for half panel\n'''
        )
        try:
            TILECOUNT = float(i)
            j = str(TILECOUNT).split('.')
            if len(j) == 1:  # Whole number case (no decimal)
                x = False
                return x, int(TILECOUNT)
            elif j[1] == '0':  # Whole number case (e.g., 4.0)
                x = False
                return x, int(TILECOUNT)
            elif j[1] == '5':  # Half panel case
                x = True
                return x, int(j[0])
            elif int(j[1]) <= 4:
                print(error1)
                raise ValueError(f"Invalid panel height: {TILECOUNT}")
            elif int(j[1]) >= 6:
                print(error1)
                raise ValueError(f"Invalid panel height: {TILECOUNT}")
        except ValueError as e:
            if "could not convert" in str(e):
                print('Enter a whole number or a float value (i.e. x or x.5)')
            print(f"Error with panel height value: {i}")
            raise ValueError(f"Invalid panel height: {i}")
        except IndexError:
            x = False
            return x, int(TILECOUNT)

    # Function to adjust every other panel to get the alternating grid colors.
    def even_is_true(i):
        i = int(i)
        if (i % 2) == 0:
            x = True
        else:
            x = False
        return x

    # def fontCalFunc(i=72, j=72):
    #     x = int(min(i, j) / 2 * 0.6)
    #     return x

    def getSizeOfText(text, font):
        bbox = draw.textbbox((0, 0), text, font=font)
        return bbox[2] - bbox[0], bbox[3] - bbox[1]

    # # This function converts list to string for use in draw.text lines
    # def wLLsz(i):
    #     j = i
    #     i = ' x '.join(str(e) for e in j)
    #     return i

    # W H = larger raster / w h = smaller raster to center
    def CalcCenter(W, H, w, h):
        x = int(W / 2) - int(w / 2)
        y = int(H / 2) - int(h / 2)
        return x, y

    """ Function to add a 1 pixel border
     likely need to call open image if sending an image to the function that
     is not already open.
     Border color defaults to white, but can add color argument. 
     """

    # This defines a variables that will be updated later
    fontsFolder = 'FONT_FOLDER'

    # Checks os and updates font name
    if sys.platform.startswith('darwin'):
        fontName = 'Arial.ttf'
    elif sys.platform.startswith('win'):
        fontName = 'arial.ttf'
    elif sys.platform.startswith('linux'):
        fontName = 'DejaVuSans.ttf'
        fontsFolder = '/usr/share/fonts/truetype/dejavu'

    # whiteBorderColor = ImageColor.getcolor('white', 'RGBA')
    # altBorderColor = ImageColor.getcolor('gray', 'RGBA')

    # def makeBorder(image, color=whiteBorderColor):
    #     # border color
    #     # borderColor = ImageColor.getcolor('white', 'RGBA')
    #     try:
    #         width, height = image.size
    #         # top and bottom borders
    #         logging.debug('Start drawing top and bottom borders')
    #         for x in range(width):
    #             for y in range(1):
    #                 image.putpixel((x, y), color)
    #             for y in range(height - 1, height):
    #                 image.putpixel((x, y), color)
    #         # left and right borders
    #         logging.debug('Start drawing left and right borders')
    #         for y in range(height):
    #             for x in range(1):
    #                 image.putpixel((x, y), color)
    #             for x in range(width - 1, width):
    #                 image.putpixel((x, y), color)
    #     except ValueError:
    #         print('There is a problem with the image called to the function')

    """ Function to parse half-tile position value
    Returns the row number after which to place the half tile
    0 = top, 99 = bottom, 1 = after 1st row, 2 = after 2nd row, etc.
    """
    def parse_half_tile_position(half_tile_position_value):
        try:
            position = int(half_tile_position_value)
            return position
        except (ValueError, TypeError):
            # Default to bottom (99) if invalid
            return 99

    # Festival input pattern
    def fest_pattern_bool(i=False):
        if i == 'TRUE':
            i = True
        else:
            i = False
        return i

    fest_pattern = fest_pattern_bool(rasterDict['festival pattern'])
    # fest_pattern = fest_pattern_bool()

    # FESTIVAL TEST PATTERN -- IF SECTION

    if fest_pattern is True:
        fest_wall_width = int_validation(rasterDict['width'])
        fest_wall_height = int_validation(rasterDict['height'])
        fest_bgColor = color_validation(rasterDict['background color'])
        # fest_wall_width = int_input_validation(
        #     '\n' + 'Enter the horizontal resolution of the test pattern: '
        # )
        # fest_wall_height = int_input_validation(
        #     '\n' + 'Enter the vertical resolution of the test pattern: '
        # )
        # fest_bgColor = color_input_validation()

        overlay_color = 127, 127, 127

        # create new image
        festIm = Image.new(
            'RGBA', (fest_wall_width, fest_wall_height), fest_bgColor)

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
        drawFestPatterns.line(
            (0, 0, scale_w, scale_h), 
            fill='gray', width=line_width, joint=None)
        drawFestPatterns.line(
            (0, scale_h, scale_w, 0), 
            fill='gray', width=line_width, joint=None)

        """ TEXT OVERLAY on FEST PATTERN -- These lines draw resolution and
        label of festival test pattern.
        """
        draw = ImageDraw.Draw(festOverlaysIm)
        # Remove fontmode to use PIL's default high-quality antialiasing
        fest_res_text = wLLsz(fest_wallsize)

        # Asks user to enter a label
        fest_wall_label_text = rasterDict['raster label']
        # fest_wall_label_text = input('What label do you want? ')
        if fest_wall_label_text == '':
            fest_wall_label_text = 'fest_test_pattern'

        # updates arialFont size
        font_scale_w, font_scale_h = scale_w / 4, scale_h / 4
        # makes text bigger if wall is smaller than 300 pixels
        if min(fest_wallsize) <= 300:
            font_scale_w, font_scale_h = scale_w / 2, scale_h / 2
        arialFont = ImageFont.truetype(
            os.path.join(fontsFolder, fontName), 
            fontCalFunc(font_scale_w, font_scale_h))
        
        # define vars for function that draws resolution text overlay
        W, H, = scale_w, scale_h
        w, h = getSizeOfText(fest_res_text, arialFont)
        text_size = CalcCenter(W, H, w, h)
        text_x, text_y = text_size
        text_y = text_y + h
        text_size = text_x, text_y

        # draws fest res text
        draw.text(
            text_size, fest_res_text, fill='white', font=arialFont)

        # updates arialFont size for title overlay text
        font_scale_w, font_scale_h = scale_w / 4.5, scale_h / 4.5
        if min(fest_wallsize) <= 300:
            font_scale_w, font_scale_h = scale_w / 2, scale_h / 2
        arialTitleFont = ImageFont.truetype(
            os.path.join(fontsFolder, fontName), 
            fontCalFunc(font_scale_w, font_scale_h))

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
        fileName = f'{fest_wall_label_text}.png'
        festIm.save(os.path.join(imageDir, fileName))

        return festIm

        # exit program if fest pattern is true
        exit()

    # Ask for user input of LED tile dimensions and bg color
    tileResWidth = int_validation(rasterDict['tile width'])
    tileResHeight = int_validation(rasterDict['tile height'])

    """ color is asked for in the color_input_validation function because
        I don't know how else to verify value is correct
    """
    bgColor = color_validation(rasterDict['background color'])

    # Log prints out summary of values captured for debugging's sake.
    # logging.debug(
        # '\n' + 'Values returned to the program: ' + '\n'
        # 'tileResWidth is ' + str(tileResWidth) + '\n'
        # 'tileResHeight is ' + str(tileResHeight) + '\n'
        # 'color value is ' + str(bgColor) + '\n')

    # Create new image of LED panel color 1
    # logging.debug('Start of Create New Image ')
    ledIm = Image.new('RGBA', (tileResWidth, tileResHeight), bgColor)

    # Call make border function to add the border
    makeBorder(ledIm, altBorderColor)

    # Create new image of LED panels color 2
    # logging.debug('lightens color by some percentage')
    r, g, b, a = bgColor
    r = int(r * 0.7)
    g = int(g * 0.7)
    b = int(b * 0.7)
    bgColor2 = r, g, b, a

    # logging.debug('''Start for loop to copy panel images 
                    # (second color) ''' + str(bgColor2))

    ledIm2 = Image.new('RGBA', (tileResWidth, tileResHeight), bgColor2)
    # logging.debug('size of ledIm2 is: ' + str(ledIm2.size))

    # Call make border function to add the border to LED color panel 2
    makeBorder(ledIm2, altBorderColor)

    # Ask for user input of wall dimensions
    # logging.debug('Start tiling panels onto wall pattern')
    wallPanelWidth = int_validation(rasterDict['panels wide'])
    half_tile_bool, wallPanelHeight = half_tile_check(rasterDict['panels high'])

    if half_tile_bool is True:
        # logging.debug('half tile is TRUE')
        ledIm3_half = Image.new(
            'RGBA', (tileResWidth, int(tileResHeight / 2)), bgColor)
        ledIm4_half = Image.new(
            'RGBA', (tileResWidth, int(tileResHeight / 2)), bgColor2)
        makeBorder(ledIm3_half, altBorderColor)
        makeBorder(ledIm4_half, altBorderColor)
        """ Gets half-tile position from rasterDict
        0 = top, 99 = bottom, 1-98 = after that row number
        """
        half_tile_position = parse_half_tile_position(
            rasterDict.get('half tile top', '99'))
    else:
        pass
        # logging.debug('half tile is false')

    # logging.debug('Program continues after half_tile_bool')

    # Create new image at size of wall
    if half_tile_bool is True:
        wallIm = Image.new(
            'RGBA',
            (
                wallPanelWidth * tileResWidth,
                (wallPanelHeight * tileResHeight) + int(tileResHeight / 2),
            ),
        )
        # Calculate where the half tile row should be inserted
        if half_tile_position == 0:
            # Top position
            half_tile_y_position = 0
        elif half_tile_position >= 99:
            # Bottom position
            half_tile_y_position = wallPanelHeight * tileResHeight
        else:
            # After specified row
            # (1 = after first row, 2 = after second row, etc.)
            half_tile_y_position = half_tile_position * tileResHeight
    else:
        wallIm = Image.new('RGBA', (
            wallPanelWidth * tileResWidth, wallPanelHeight * tileResHeight))

    # logging.debug('wallIm size = ' + str(wallIm.size))
    # logging.debug('wallPanelWidth = ' + str(wallPanelWidth))
    # logging.debug('wallPanelHeight = ' + str(wallPanelHeight))
    # logging.debug('tileResWidth = ' + str(tileResWidth))
    # logging.debug('tileResHeight = ' + str(tileResHeight))

    # noqa: E302

    # FOR LOOP DRAWING LED PANELS onto wall image with alternating colors

    wallPanelWidth2, wallPanelHeight2 = wallIm.size
    tileResWidth, tileResHeight = ledIm.size

    # logging.debug('wallPanelWidth = ' + str(wallPanelWidth))
    # logging.debug('tileResWidth = ' + str(tileResWidth))
    # logging.debug(
        # 'Start for loop to copy panel images with alternating colors')
    # logging.debug(
    #     'wallPanelHeight begin loop at 213 = ' + str(wallPanelHeight))
    # logging.debug('wallPanelHeight = ' + str(wallPanelHeight2))

    # Draw full tiles with checkerboard pattern
    # If half tile is in middle, we need to draw tiles in sections

    if (half_tile_bool is True and half_tile_position > 0 and
            half_tile_position < 99):
        # Half tile is in the middle - draw in two sections
        half_tile_row_height = int(tileResHeight / 2)

        # Section 1: Draw tiles ABOVE the half tile
        # (rows 0 to half_tile_position)
        for row in range(half_tile_position):
            y_pos = row * tileResHeight
            for col in range(wallPanelWidth):
                x_pos = col * tileResWidth
                # Determine which color based on checkerboard pattern
                if (row + col) % 2 == 0:
                    wallIm.paste(ledIm, (x_pos, y_pos))
                else:
                    wallIm.paste(ledIm2, (x_pos, y_pos))

        # Section 2: Draw tiles BELOW the half tile (remaining rows)
        # These start after the half tile row
        for row in range(half_tile_position, wallPanelHeight):
            y_pos = (row * tileResHeight) + half_tile_row_height
            for col in range(wallPanelWidth):
                x_pos = col * tileResWidth
                # Determine which color based on checkerboard pattern
                # Add 1 to row since these tiles are visually one row below
                # the half tile (which acts as row 'half_tile_position')
                pattern_row = row + 1
                if (pattern_row + col) % 2 == 0:
                    wallIm.paste(ledIm, (x_pos, y_pos))
                else:
                    wallIm.paste(ledIm2, (x_pos, y_pos))

    elif half_tile_bool is True and half_tile_position == 0:
        # Half tile on top - shift all full tiles down
        half_tile_row_height = int(tileResHeight / 2)
        for row in range(wallPanelHeight):
            y_pos = (row * tileResHeight) + half_tile_row_height
            for col in range(wallPanelWidth):
                x_pos = col * tileResWidth
                # Determine which color based on checkerboard pattern
                # Add 1 to row since these tiles are visually one row below
                # the half tile at row 0
                pattern_row = row + 1
                if (pattern_row + col) % 2 == 0:
                    wallIm.paste(ledIm, (x_pos, y_pos))
                else:
                    wallIm.paste(ledIm2, (x_pos, y_pos))

    else:
        # Half tile on bottom or no half tile - draw normally
        top_start = 0
        top_start_alt = tileResHeight

        for left in range(0, wallPanelWidth2, tileResWidth * 2):
            for top in range(top_start, wallPanelHeight2, tileResHeight * 2):
                wallIm.paste(ledIm, (left, top))
        for leftAlt in range(tileResWidth, wallPanelWidth2, tileResWidth * 2):
            for topAlt in range(top_start_alt, wallPanelHeight2,
                                tileResHeight * 2):
                wallIm.paste(ledIm, (leftAlt, topAlt))
        for left in range(0, wallPanelWidth2, tileResWidth * 2):
            for top in range(top_start_alt, wallPanelHeight2,
                             tileResHeight * 2):
                wallIm.paste(ledIm2, (left, top))
        for leftAlt in range(tileResWidth, wallPanelWidth2, tileResWidth * 2):
            for topAlt in range(top_start, wallPanelHeight2,
                                tileResHeight * 2):
                wallIm.paste(ledIm2, (leftAlt, topAlt))

    # logging.debug('wallPanelHeight begin loop at 431 = ' + str(wallPanelHeight))
    # logging.debug('wallPanelHeight = ' + str(wallPanelHeight2))

    #
    #
    """ HALF PANELS -- Draws half-panels onto the wall image and
    alternates half-panel colors
    """

    if half_tile_bool is True:
        # Draw half tiles with alternating colors across the row
        # The half tile row should alternate from the row above it
        for col in range(wallPanelWidth):
            x_pos = col * tileResWidth
            y_pos = half_tile_y_position

            # Determine which color based on checkerboard pattern
            # The row number for pattern purposes depends on position
            if half_tile_position == 0:
                # Top position - row 0 in the pattern
                pattern_row = 0
            elif half_tile_position >= 99:
                # Bottom position - after all full rows
                # Pattern continues from wallPanelHeight
                pattern_row = wallPanelHeight
            else:
                # Middle position - after row N
                # This is effectively row N in the pattern
                # (which will alternate from row N-1 above it)
                pattern_row = half_tile_position

            # Checkerboard: if (row + col) is even, use color 1, else color 2
            if (pattern_row + col) % 2 == 0:
                wallIm.paste(ledIm3_half, (x_pos, y_pos))
            else:
                wallIm.paste(ledIm4_half, (x_pos, y_pos))

    # logging.debug('For loop A copying led panels to wall complete')
    # logging.debug('tileResWidth 141 = ' + str(tileResWidth))
    # logging.debug('tileResHeight 142 = ' + str(tileResHeight))
    # logging.debug('wallPanelHeight = ' + str(wallPanelHeight))
    # logging.debug('wallPanelHeight = ' + str(wallPanelHeight2))

    # creating variables to loop later - also centering the text
    draw = ImageDraw.Draw(wallIm)
    # Remove fontmode to use PIL's default high-quality antialiasing
    W, H, half_H = (tileResWidth, tileResHeight, (tileResHeight / 2))

    # logging.debug('W = ' + str(W) + 'H = ' + str(H) + 'half_H = ' + str(half_H))

    """ these variables are defined outside the loops
        so they can be manipulated
        List (needs to be converted to string for use)
    """

    indexNums = [i_offset_0, i_offset_1]

    # This function converts list to string for use in draw.text lines

    def iNc(i):
        i = ','.join(str(e) for e in indexNums)
        return i

    # calculate appropriate font size for panel resolution
    fontCal = int(min(tileResHeight, tileResWidth) / 2 * 0.6)
    arialFont = ImageFont.truetype(os.path.join(fontsFolder, fontName), fontCal)

    """ calculates the width and height of text to be drawn
        function below added later -- can eventually replace
        '# original line that calculates' line but rest of code 
        will need to be updated.
    """

    # original line that calculates the width and height of text to be drawn
    _bbox = draw.textbbox((0, 0), iNc(indexNums), font=arialFont)
    w, h = _bbox[2] - _bbox[0], _bbox[3] - _bbox[1]

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
        # logging.debug('Start while true')
        loop_counter1 = 0

        # original while statement
        # while indexNums[0] <= wallPanelWidth + 1:

        while indexNums[0] <= wallPanelWidth + i_offset_0:

            loop_counter1 += 1

            # Draw half tile text at the start if position is 0
            if (half_tile_bool is True and half_tile_position == 0 and
                    indexNums[1] == 1):
                # Calculate position for half tile text at top
                adjusted_x_coord_for_text_halfpanel = (
                    (W - w) / 2) + (indexNums[0] - i_offset_0) * tileResWidth
                adjusted_y_coord_for_text_halfpanel = (
                    half_tile_y_position + ((half_H - h) / 2))

                # Create special index for half tile at row 1 (display starts at 1)
                half_tile_indexNums = [indexNums[0], 1]
                half_tile_text = ','.join(
                    str(e) for e in half_tile_indexNums)
                # calculates the width and height of text
                _bbox = draw.textbbox((0, 0), half_tile_text, font=arialFont)
                w_half, h_half = _bbox[2] - _bbox[0], _bbox[3] - _bbox[1]
                # draws text on the half panel at top
                draw.text(
                    (adjusted_x_coord_for_text_halfpanel,
                     adjusted_y_coord_for_text_halfpanel,),
                    half_tile_text,
                    fill='gray',
                    font=arialFont)

            # logging.debug('While 1 statement start. ' + str(loop_counter1) + str(' ') + str(indexNums))

            # Determine display row number (may differ from indexNums[1])
            display_row_num = indexNums[1]

            # Determine Y offset and row numbering based on half tile location
            y_offset_adjust = 0
            if half_tile_bool is True:
                if half_tile_position == 0:
                    # Half tile on top - shift all text down
                    y_offset_adjust = tileResHeight / 2
                    # Row numbers increment (half tile is row 1, so full tiles are 2, 3, 4...)
                    display_row_num = indexNums[1] + 1
                elif (half_tile_position < 99 and
                      indexNums[1] > half_tile_position):
                    # Half tile in middle - shift text below it down
                    y_offset_adjust = tileResHeight / 2
                    # Row numbers increment after the half tile
                    display_row_num = indexNums[1] + 1

            # Create display text and measure it before computing position
            # so that position always uses the actual width of the current text
            display_indexNums = [indexNums[0], display_row_num]
            display_text = ','.join(str(e) for e in display_indexNums)
            _bbox = draw.textbbox((0, 0), display_text, font=arialFont)
            w, h = _bbox[2] - _bbox[0], _bbox[3] - _bbox[1]

            adjusted_x_coord_for_text = (
                (W - w) / 2) + (indexNums[0] - i_offset_0) * tileResWidth
            adjusted_y_coord_for_text = (
                (H - h) / 2) + (indexNums[1] - i_offset_1) * tileResHeight + y_offset_adjust

            # adds more text to half panels if they exist
            if half_tile_bool is True:
                adjusted_x_coord_for_text_halfpanel = (
                    (W - w) / 2) + (indexNums[0] - i_offset_0) * tileResWidth
                adjusted_y_coord_for_text_halfpanel = (
                    half_tile_y_position + ((half_H - h) / 2))

            # draws text
            draw.text(
                (adjusted_x_coord_for_text, adjusted_y_coord_for_text),
                display_text,
                fill='gray',
                font=arialFont)

            # adds to index number
            indexNums[1] += 1

            # logging.debug('indexNums update 370 ' + str(indexNums))

            # This if statements draws the half-tile numbers
            if half_tile_bool is True:
                # logging.debug('Begin drawing half-tile text ')

                # Determine which row should have half-tile text
                should_draw_half_tile_text = False
                half_tile_display_row = None

                # Position 0 is handled earlier in the loop
                if (half_tile_position > 0 and half_tile_position < 99 and
                        indexNums[1] == half_tile_position + 1):
                    # Half tile is in the middle after specified row
                    should_draw_half_tile_text = True
                    half_tile_display_row = half_tile_position + 1
                elif (half_tile_position >= 99 and
                      indexNums[1] == wallPanelHeight + 1):
                    # Half tile is on bottom
                    should_draw_half_tile_text = True
                    half_tile_display_row = wallPanelHeight + 1

                if (should_draw_half_tile_text and
                        half_tile_display_row is not None):
                    # Create special index for half tile
                    half_tile_indexNums = [indexNums[0], half_tile_display_row]
                    half_tile_text = ','.join(
                        str(e) for e in half_tile_indexNums)
                    # calculates the width and height of text
                    _bbox = draw.textbbox((0, 0), half_tile_text, font=arialFont)
                    w, h = _bbox[2] - _bbox[0], _bbox[3] - _bbox[1]
                    # draws text on the half panel
                    draw.text(
                        (adjusted_x_coord_for_text_halfpanel,
                         adjusted_y_coord_for_text_halfpanel,),
                        half_tile_text,
                        fill='gray',
                        font=arialFont)
                # logging.debug('END IF statement LOWER drawing half-tile text ' + str(indexNums))
                # logging.debug('iNc function output = ' + str(iNc(indexNums)))
                # logging.debug(
                #     'adjusted_x_coord_for_text_halfpanel = ' + str(adjusted_x_coord_for_text_halfpanel)
                # )
                # logging.debug(
                #     'adjusted_y_coord_for_text_halfpanel = ' + str(adjusted_y_coord_for_text_halfpanel)
                # )
                # logging.debug('adjusted_x_coord_for_text = ' + str(adjusted_x_coord_for_text))
                # logging.debug('adjusted_y_coord_for_text = ' + str(adjusted_y_coord_for_text) + '\n')

            # original if statement
            if indexNums[1] == wallPanelHeight + 1:
                # logging.debug('Start if indexNums A. ' + str(indexNums))

                # these are necessary to prevent infinite loop
                indexNums[0] += 1
                indexNums[1] = 1

                adjusted_x_coord_for_text = CENT_X_CORD_FOR_TEXT
                adjusted_y_coord_for_text += tileResHeight

                # calculates the width and height of text to be drawn
                _bbox = draw.textbbox((0, 0), iNc(indexNums), font=arialFont)
                w, h = _bbox[2] - _bbox[0], _bbox[3] - _bbox[1]
                # logging.debug('draw.textsize w value = ' + str(w) + '-- h value = ' + str(h))

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
    LED_wall_label_text = rasterDict['raster label']
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

    # saves image file
    fileName = f'{LED_wall_label_text}.png'
    wallIm.save(os.path.join(imageDir, fileName))

    # logging.debug(
    #     'wallPanelWidth value is: ' + str(wallPanelWidth) + 
    #     '\n END OF PROGRAM \n \n \n')
    return wallIm   


if __name__ == "__main__":
    make_raster()  # Call main() if this module is run, but not when imported.
