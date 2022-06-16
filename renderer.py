import math
import os

class Camera:
    def __init__(self, anchor, camW, camH, screen):
        self.anchor = anchor
        self.camW = camW
        self.camH = camH
        self.screen = screen
    def clearEdgeClipping(self):
        
        if self.anchor[0] < 0:
            self.anchor[0] = 0
        if self.anchor[1] < 0:
            self.anchor[1] = 0
        if self.screen.screenW < self.anchor[0] + self.camW:
            self.anchor[0] = self.screen.screenW - self.camW
        if self.screen.screenH < self.anchor[1] + self.camH:
            self.anchor[1] = self.screen.screenH - self.camH
        
    def printScreen(self):
        anchor2w = self.anchor[0] + self.camW
        anchor2h = self.anchor[1] + self.camH
        
        os.system('clear')
        
        for row in self.screen.renderedFrame[self.anchor[1]:anchor2h]:
            rowString = ''
            for c in row[self.anchor[0]:anchor2w]:
                rowString = rowString + c
            print(rowString)
class Screen:
    def __init__(self, screenW, screenH):
        self.screenW = screenW
        self.screenH = screenH
        self.renderedFrame = []
    def clearScreen(self):
        os.system('clear')
        self.renderedFrame = []

            
class Renderer:
    def __init__(self, screen, char):
        self.screen = screen
        self.char = char
    def renderFrame(self, frame):
        dArray = []
        for h in range(0, self.screen.screenH):
            currentRow = []
            for w in range(0, self.screen.screenW):
                currentRow.append(self.char)
            dArray.append(currentRow)
        for h in range(0, self.screen.screenH):
            for w in range(0, self.screen.screenW):
                for o in frame.objects:
                    if str([w, h]) in o.points.keys():
                        try:
                            dArray[h][w] = o.points[str([w, h])]
                        except:
                            pass
        self.screen.renderedFrame = dArray
        
class Frame:
    def __init__(self, objects):
        self.objects = objects
    def insert(self, indexToInsert, objectToInsert):
        self.objects.insert(indexToInsert, objectToInsert)

class Shape: #this is moderately useless but a great organization method so i say def keep nested
    class Point:
        def __init__(self, x, y, char):
            self.points = {}
            self.x = x
            self.y = y
            self.char = char
            self.points.update({str([x, y]): self.char})
        def update(self):
            self.points = {}
            self.points.update({str([self.x, self.y]): self.char})

    class Text:
        def __init__(self, x, y, string):
            self.x = x
            self.y = y
            self.string = string
            self.points = {}
            xCounter = x
            for c in string:
                self.points.update({str([xCounter, y]): c})
                xCounter += 1
        def update(self):
            xCounter = self.x
            for c in self.string:
                self.points.update({str([xCounter, self.y]): c})
                xCounter += 1

    class Rectangle:
        def __init__(self, width, height, topLeftCoord, char):
            self.width = width
            self.height = height
            self.topLeftCoord = topLeftCoord
            self.char = char
            self.points = {}
            for i in range(topLeftCoord[0], topLeftCoord[0] + width): #did i make this i dont remember
                for j in range(topLeftCoord[1], topLeftCoord[1] + height):
                    self.points.update({str([i, j]): char})
        def update(self):
            self.points = {}
            for i in range(self.topLeftCoord[0], self.topLeftCoord[0] + self.width): #did i make this i dont remember
                for j in range(self.topLeftCoord[1], self.topLeftCoord[1] + self.height):
                    self.points.update({str([i, j]): self.char})

    class Overlay:
        def __init__(self, anchor, dArray):
            self.anchor = anchor
            self.dArray = dArray
            self.points = {}
            hCounter = 0
            for h in dArray:
                wCounter = 0
                for w in h:
                    self.points.update({str([wCounter + anchor[0], hCounter + anchor[1]]): w})
                    wCounter += 1
                hCounter += 1
        def update(self):
            self.points = {}
            hCounter = 0
            for h in self.dArray:
                wCounter = 0
                for w in h:
                    self.points.update({str([wCounter + self.anchor[0], hCounter + self.anchor[1]]): w})
                    wCounter += 1
                hCounter += 1               