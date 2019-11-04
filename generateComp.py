import sys 
from PIL import Image, ImageDraw
import random

MAX_WIDTH = 2121
MAX_HEIGHT = 1414

random.seed()

def generateColor():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def generateBackgroundPartial(draw):
    corners = [(0, 0), (MAX_WIDTH, 0), (0, MAX_HEIGHT), (MAX_WIDTH, MAX_HEIGHT)]

    random.shuffle(corners)

    corner1 = corners.pop(0)

    for point in corners:
        if point[0] == corner1[0] or point[1] == corner1[1]:
            corner2 = point
            break

    if corner1[1] == corner2[1]:
        x_cord1 = corner1[0]
        x_cord2 = corner2[0]
        y_cord1 = random.randint(0, MAX_HEIGHT)
        y_cord2 = random.randint(0, MAX_HEIGHT)
    else:
        x_cord1 = random.randint(0, MAX_WIDTH)
        x_cord2 = random.randint(0, MAX_WIDTH)
        y_cord1 = corner2[1]
        y_cord2 = corner2[1]

    cord1 = (x_cord1, y_cord1)
    cord2 = (x_cord2, y_cord2)
    
    return draw.polygon([corner1, corner2, cord2, cord1], generateColor())

def generateRandomLine(draw):
    minLineWidth = 20
    maxLineWidth = 80
    cord1 = (random.randint(0, MAX_WIDTH), random.randint(0, MAX_HEIGHT))
    cord2 = (random.randint(0, MAX_WIDTH), random.randint(0, MAX_HEIGHT))
    return draw.line([cord1, cord2], generateColor(), random.randint(minLineWidth, maxLineWidth))

def generateRandomTriangle(draw):
    cord1 = (random.randint(0, MAX_WIDTH), random.randint(0, MAX_HEIGHT))
    cord2 = (random.randint(0, MAX_WIDTH), random.randint(0, MAX_HEIGHT))
    cord3 = (random.randint(0, MAX_WIDTH), random.randint(0, MAX_HEIGHT))
    return draw.polygon([cord1, cord2, cord3], generateColor())

print("Test")

#Generates the base image
img = Image.new('RGB', (MAX_WIDTH, MAX_HEIGHT), color = generateColor())
draw = ImageDraw.Draw(img)

maxPartial = 1
for i in range(random.randint(0, maxPartial)):
    generateBackgroundPartial(draw)

maxLineNum = 3
for i in range(random.randint(0, maxLineNum)):
    generateRandomLine(draw)

maxTriangleNum = 3
for i in range(random.randint(0, maxTriangleNum)):
    generateRandomTriangle(draw)

img.save('./python/color.png')
