#! python3
# greyStepsPatternMaker.py

# Test pattern generator for checking color space

# logging
import logging
from PIL import Image, ImageDraw, ImageFont, ImageColor
import os


logging.basicConfig(
    filename='greyStepsPatternLog.txt',
    level=logging.DEBUG,
    format=' %(asctime)s - %(levelname)s - %(message)s',
)
# disables logging when uncommented
#logging.disable(logging.CRITICAL)
logging.debug('\n' + ' \n' + '\n' + '********** START OF PROGRAM **********')

# This defines a variables that will be updated later
# fontsFolder = 'FONT_FOLDER'
# rgb = (0, 0, 0)
# grey steps need to default to 12 and them bump to 16 if resolution larger than 1920x1080
# greySteps = 12
LIMITED_LOW_VALUE = (16, 16, 16)
LIMITED_HIGH_VALUE = (235, 235, 235)
FULL_LOW_VALUE = (0, 0, 0)
FULL_HIGH_VALUE = (255, 255, 255)
# lowIndex = round((greySteps / 4) - 1)
# highIndex = round(greySteps - (greySteps / 4) - 1)
# middleRange = int(greySteps / 2)
# outerRange = greySteps - (highIndex + 1)
# logging.debug('greySteps 1 = ' + str(greySteps))

# Function to validate resolution input
def int_input_validation(prompt):
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print('You need to enter a non-negative integer (a whole number) ')
            # better try again ... return to the start of the loop
            continue
        else:
            # input successfully parsed!
            # we're ready to exit the loop.
            break
    return value 


def greyBlockWidth(rasterWidth):
    blockWidth = rasterWidth / (greySteps - 1)
    return round(blockWidth)


def rgbOuterRangeStepper(rgb, greySteps):
    global LIMITED_LOW_VALUE
    rgb = list(rgb)
    newRgbList = []
    for i in rgb:
        i += round(LIMITED_LOW_VALUE[0] / 2)
        newRgbList.append(i)
    return tuple(newRgbList)


def rgbInnerRangeStepper(rgb, greySteps):
    global LIMITED_LOW_VALUE
    global LIMITED_HIGH_VALUE
    rgb = list(rgb)
    newRgbList = []
    for i in rgb:
        i += round((LIMITED_HIGH_VALUE[0] - LIMITED_LOW_VALUE[0]) / greySteps)
        newRgbList.append(i)
    return tuple(newRgbList)


# def fontCalFunc(i=14, j=14):
#     x = int(min(i, j) / 2 * 0.6)
#     return x 


def getSizeOfText(text, font):
    w, h = draw.textsize(text, font)
    return w, h 


def stepValue(startValue, maxValue, steps):
    eachStepValue = (maxValue - startValue) / (steps)
    currentStep = startValue
    stepList = [startValue]
    while currentStep < (maxValue):
        currentStep += eachStepValue
        stepList.append(int(currentStep))
    stepList[-1] = maxValue
    return stepList


def innerStepValue(startValue, maxValue, steps):
    eachStepValue = int((maxValue - startValue) / (steps))
    currentStep = startValue
    stepList = [startValue]
    logging.debug('max value input into function = ' + str(maxValue))
    logging.debug('currentStep 1 (start) = ' + str(currentStep))
    logging.debug('each step value = ' + str(eachStepValue))
    for i in range(middleRange):
        currentStep += eachStepValue
        logging.debug('currentStep itr2 = ' + str(currentStep))
        stepList.append(int(currentStep))
    stepList[-1] = maxValue
    return stepList


def rgbTupleMaker(value):
    rgb = [value, value, value]
    rgb = tuple(rgb)
    return rgb


def textBgHeight(wall_height):
    x = wall_height * 0.058
    y = int(x)
    return y


def LimTextBgHeight(wall_height):
    x = wall_height * 0.095
    y = int(x)
    return y


def textBgLimitedWidth(wall_width):
    global outerRange
    global blockWidth
    global middleRange
    global lowIndex
    x = blockWidth * (middleRange + 1)
    return x

new line to test 

def fontCalFunc(i=14, j=14):
    x = int(min(i, j) / 26)
    return x


def getSizeOfText(text, font):
    w, h = draw.textsize(text, font)
    return w, h


def stepDivAdj(wall_width, greySteps):
    if 1920 < wall_width <= 3840:
        greySteps = 16
    elif wall_width > 3840:
        greySteps = 24
    return greySteps


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

# User input
wall_width = int_input_validation(
    '\n' + 'Enter the horizontal resolution of the test pattern: '
    )
wall_height = int_input_validation(
    '\n' + 'Enter the vertical resolution of the test pattern: '
    )


# Variables
fontsFolder = 'FONT_FOLDER'
rgb = (0, 0, 0)
# grey steps need to default to 12 and them bump to 16 if resolution larger than 1920x1080
greySteps = 12
logging.debug('greySteps before function = ' + str(greySteps))
# adjuststs grey steps based on resolution
greySteps = stepDivAdj(wall_width, greySteps)
logging.debug('greySteps after function = ' + str(greySteps))
lowIndex = round((greySteps / 4) - 1)
highIndex = round(greySteps - (greySteps / 4) - 1)
middleRange = int(greySteps / 2)
outerRange = greySteps - (highIndex + 1)
blockWidth = greyBlockWidth(wall_width)

logging.debug(
    '\n' + '\t' + 'wall width = ' + str(wall_width) +
    '\n' + '\t' + 'wall height = ' + str(wall_height) +
    '\n' + '\t' + 'block width = ' + str(blockWidth) +
    '\n' + '\t' + 'lowIndex = ' + str(lowIndex) +
    '\n' + '\t' + 'middleRange = ' + str(middleRange) +
    '\n' + '\t' + 'highIndex = ' + str(highIndex) + 
    '\n' + '\t' + 'outerRange = ' + str(outerRange)
    )

# create new image as the background
greyIm = Image.new('RGBA', (wall_width, wall_height), (rgb))

# make RGB list for updating color
rgbList = []
rgbTupleList = []
lowRangeLst = stepValue(FULL_LOW_VALUE[0], LIMITED_LOW_VALUE[0], lowIndex)
for i in enumerate(lowRangeLst):
    logging.debug('lowRangeLst -- ' + str(i))
hiRangeLst = stepValue(LIMITED_HIGH_VALUE[0], FULL_HIGH_VALUE[0], lowIndex)
for i in enumerate(hiRangeLst):
    logging.debug('hiRangeLst -- ' + str(i))
middleLst = innerStepValue(LIMITED_LOW_VALUE[0], LIMITED_HIGH_VALUE[0], middleRange)
for i in enumerate(middleLst):
    logging.debug('middleLst -- ' + str(i))       
middleLst = middleLst[1:-1]
rgbList = lowRangeLst + middleLst + hiRangeLst
logging.debug('\n')
for i in enumerate(rgbList):
    logging.debug('rgb enumerated -- ' + str(i))
logging.debug('\n')
for i in rgbList:
    rgbTupleList.append(rgbTupleMaker(i))
for i in enumerate(rgbTupleList):
    logging.debug('rgb tuple list -- ' + str(i))

# paste step images
greyIndex = 1
xPos = 0
logging.debug('xPos = ' + str(xPos))
while xPos < wall_width:
    greyStep = Image.new('RGBA', (blockWidth, wall_height), (rgbTupleList.pop(0)))
    greyIm.paste(greyStep, (xPos, 0))
    xPos += blockWidth
    greyIndex += 1

# text-blocks BG for titles
textBgH = textBgHeight(wall_height)
LimTextBgH = LimTextBgHeight(wall_height)
LimTextBgW = textBgLimitedWidth(wall_width)
LimTextBgXpos = blockWidth * lowIndex
LimTextBgYpos = textBgH
fullTextBlockBlack = Image.new('RGBA', (wall_width, textBgH), (0, 0, 0))
limitedTextBlockBlack = Image.new('RGBA', (LimTextBgW, LimTextBgH), (0, 0, 0, 220))
greyIm.paste(fullTextBlockBlack, (0,0))
logging.debug('LimTextBgXpos = ' + str(LimTextBgXpos))
logging.debug('LimTextBgYpos = ' + str(LimTextBgYpos))
logging.debug('Lim Text Bg Width = ' + str(LimTextBgW))
greyIm.alpha_composite(limitedTextBlockBlack, (LimTextBgXpos, LimTextBgYpos))

# text-block text ____________________________
# imageSize = greyIm.size
draw = ImageDraw.Draw(greyIm)
draw.fontmode = 'L'
textString = 'Full Range'
#update arialFont size
arialFont = ImageFont.truetype(
    os.path.join(fontsFolder, 'Arial.ttf'), fontCalFunc(wall_width, wall_height)
)
# define vars for function that draws full text
W, H, = wall_width, wall_height
w, h = getSizeOfText(textString, arialFont)
textPos = CalcCenter(W, H, w, h)
text_x, text_y = textPos
text_y = wall_height - (wall_height * 0.99)
textPos = text_x, text_y
draw.text(textPos, textString, fill='white', font=arialFont)

# update vars and draw limited text
textString = 'Limited'
w, h = getSizeOfText(textString, arialFont)
textPos = CalcCenter(W, H, w, h)
text_x, text_y = textPos
text_y = wall_height - (wall_height * 0.895)
textPos = text_x, text_y
draw.text(textPos, textString, fill='grey', font=arialFont)

# update vars and draw bar brightness value text
w, h = getSizeOfText(textString, arialFont)
text_x = blockWidth / 2
text_spacer = blockWidth / 2
loopCounter = 1
logging.debug('rgbList = ' + str(rgbList))
for i in rgbList:
    # textString = i
    fillColor = 'grey'
    if loopCounter > highIndex + 1:
        fillColor='black' 
    textString = str(i)
    w, h = getSizeOfText(textString, arialFont)
    textPos = CalcCenter(W, H, w, h)
    text_x, text_y = textPos
    text_y = wall_height - (wall_height * 0.94)
    text_x = (blockWidth * loopCounter) - (blockWidth / 2) - (w / 2)
    textPos = text_x, text_y
    draw.text(textPos, textString, fill=fillColor, font=arialFont)
    # text_x += blockWidth
    loopCounter += 1


# saves image file
greyIm.save('greyTestPattern.png')














