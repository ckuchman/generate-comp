import sys
import random
import math
from PIL import Image, ImageDraw


MAX_WIDTH = 2121
MAX_HEIGHT = 1414

random.seed()


#----------Classes----------
class Shape:
    def __init__(self, color):
        self.color = color


class Line(Shape):
    def __init__(self, color, thickness, cord1, cord2):
        super().__init__(color)
        self.thickness = thickness
        self.cord1 = cord1
        self.cord2 = cord2

    def draw(self, img):
        ImageDraw.Draw(img).line([self.cord1, self.cord2], self.color, self.thickness)


class Triangle(Shape):
    def __init__(self, color, cord1, cord2, cord3):
        super().__init__(color)
        self.cord1 = cord1
        self.cord2 = cord2
        self.cord3 = cord3

    def draw(self, img):
        ImageDraw.Draw(img).polygon([self.cord1, self.cord2, self.cord3], self.color)


class PerspectiveCube(Shape):
    def __init__(self, color, origin, width, height):
        super().__init__(color)
        self.origin = origin
        self.width = width
        self.height = height

    def draw(self, img, vanPnt):
        widthPnt = (self.origin[0] + self.width, self.origin[1])
        heightPnt = (self.origin[0], self.origin[1] + self.height)
        oppPnt = (self.origin[0] + self.width, self.origin[1] + self.height)

        draw.polygon([self.origin, heightPnt, oppPnt, widthPnt], self.color)

#----------Functions----------
def genColor():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def genRandomCord(xMinRange, xMaxRange, yMinRange, yMaxRange):
    #Range is used to indicate where to constrain the shape with 1 being the full screen, numbers
    #above 1 are allowed to have shapes go off screen (so a 2 xMinRange would allow double the safe
    #to the left of the screen.
    
    xCordRange = math.floor(MAX_WIDTH + ((xMaxRange - 1) * MAX_WIDTH) + ((xMinRange - 1) * MAX_WIDTH))
    xCord = math.floor(random.randint(0, xCordRange) - ((xMinRange - 1) * MAX_WIDTH))

    yCordRange = math.floor(MAX_HEIGHT + ((yMaxRange - 1) * MAX_HEIGHT) - ((yMinRange - 1) * MAX_HEIGHT))
    yCord = math.floor(random.randint(0, yCordRange) - ((yMinRange - 1) * MAX_HEIGHT))
    
    return (xCord, yCord)


def genBackgroundPartial(draw):
    corners = [(0, 0), (MAX_WIDTH, 0), (0, MAX_HEIGHT), (MAX_WIDTH, MAX_HEIGHT)]

    random.shuffle(corners)

    corner1 = corners.pop(0)

    for point in corners:
        if point[0] == corner1[0] or point[1] == corner1[1]:
            corner2 = point
            break

    if corner1[1] == corner2[1]:
        xCord1 = corner1[0]
        xCord2 = corner2[0]
        yCord1 = random.randint(0, MAX_HEIGHT)
        yCord2 = random.randint(0, MAX_HEIGHT)
    else:
        xCord1 = random.randint(0, MAX_WIDTH)
        xCord2 = random.randint(0, MAX_WIDTH)
        yCord1 = corner1[1]
        yCord2 = corner2[1]

    cord1 = (xCord1, yCord1)
    cord2 = (xCord2, yCord2)
    
    return draw.polygon([corner1, corner2, cord2, cord1], genColor())


def genRandomLine():
    minLineWidth = 20
    maxLineWidth = 80
    cord1 = genRandomCord(1.5, 1.5, 1.5, 1.5)
    cord2 = genRandomCord(1.5, 1.5, 1.5, 1.5)

    return Line(genColor(), random.randint(minLineWidth, maxLineWidth), cord1, cord2)


def genRandomTriangle():
    cord1 = genRandomCord(1.25, 1.25, 1.25, 1.25)
    cord2 = genRandomCord(1.25, 1.25, 1.25, 1.25)
    cord3 = genRandomCord(1.25, 1.25, 1.25, 1.25)

    return Triangle(genColor(), cord1, cord2, cord3)


def genHorizon(draw, height): 
    return draw.polygon([(0,0), (0,height), (MAX_WIDTH, height), (MAX_WIDTH, 0)], genColor())


def genOnePointPerspective(draw, height):
    xCord = random.randint(0, MAX_WIDTH)
    
    return (xCord, height)


#----------Main Functions----------
def randomImage():
    #gens the base image
    img = Image.new('RGB', (MAX_WIDTH, MAX_HEIGHT), color = genColor())
    draw = ImageDraw.Draw(img)

    maxPartial = 2
    for i in range(random.randint(0, maxPartial)):
        genBackgroundPartial(draw)

    shapeList = []

    maxLineNum = 3
    for i in range(random.randint(0, maxLineNum)):
        shapeList.append(genRandomLine())

    maxTriangleNum = 3
    for i in range(random.randint(0, maxTriangleNum)):
        shapeList.append(genRandomTriangle())

    for shp in shapeList:
        shp.draw(img)

    img.save('color.png')


def perspectiveImage():
    #gens the base image
    img = Image.new('RGB', (MAX_WIDTH, MAX_HEIGHT), color = genColor())
    draw = ImageDraw.Draw(img)

    height = random.randint(0, MAX_HEIGHT)
    genHorizon(draw, height)
    vanPnt = genOnePointPerspective(draw, height)

    cube = PerspectiveCube(genColor(), (1000, 1000), 100, 200)
    cube.draw(img, vanPnt)

    shapeList = []

    for shp in shapeList:
        shp.draw(img)

    img.save('horizon.png')

#----------Main----------
perspectiveImage()
