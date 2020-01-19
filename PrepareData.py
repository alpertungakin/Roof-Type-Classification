from tkinter.filedialog import askopenfilename as ask
import os
os.environ['OPENCV_IO_MAX_IMAGE_PIXELS']=str(2**64)
from cv2 import cv2
import numpy as np
import json
import geopandas as gpd

class PrepareData():
    def __init__(self):
        self.executeMode = input("Declare mode of execution (TestData/TrainData): ")
        self.worldFile = open(ask(title = "Select World File"),"r")
        self.worldRaw = self.worldFile.read()
        self.worldFile.close()
        self.imagepath = ask(title = "Select Image File")
        self.ImageInContext = cv2.imread(self.imagepath, cv2.IMREAD_COLOR)
        self.shapePath = ask(title = "Select ShapeFile")
        self.buildShape = gpd.read_file(self.shapePath)
        self.worldInformation()
        self.handleImage()
        self.createWorldFiles()
        
    def worldInformation(self):
        self.X = float(self.worldRaw.split("\n")[4])
        self.Y = float(self.worldRaw.split("\n")[5])
        self.Xsize = float(self.worldRaw.split("\n")[0])
        self.Ysize = float(self.worldRaw.split("\n")[3])
        self.worldInfo = [self.X, self.Y, self.Xsize, self.Ysize]

    def handleImage(self):
        self.boundingBoxes = [[], [], [], []]
        print("Building Borders Calculating...")
        for shp in range(len(self.buildShape)):
            self.boundingBoxes[0].append(int((self.buildShape.envelope[shp].bounds[0]-self.X)/self.Xsize))
            self.boundingBoxes[1].append(int((self.buildShape.envelope[shp].bounds[1]-self.Y)/self.Ysize))
            self.boundingBoxes[2].append(int((self.buildShape.envelope[shp].bounds[2]-self.X)/self.Xsize))
            self.boundingBoxes[3].append(int((self.buildShape.envelope[shp].bounds[3]-self.Y)/self.Ysize))
        for i in range(len(self.buildShape)):
            cv2.imwrite("{}/{}_{}.jpg".format(self.executeMode, self.buildShape.Polygon_ID[i],self.buildShape.Image_Name[0]), self.ImageInContext[self.boundingBoxes[3][i]:self.boundingBoxes[1][i], self.boundingBoxes[0][i]:self.boundingBoxes[2][i]])
        print("Calculated!")

    def createWorldFiles(self):
        for k in range(len(self.buildShape)):
            with open('{}/{}_{}.txt'.format(self.executeMode, self.buildShape.Polygon_ID[k], self.buildShape.Image_Name[0]),'w') as f:
                json.dump({"Upper Left X":self.buildShape.envelope[k].bounds[0], "Upper Left Y: ":self.buildShape.envelope[k].bounds[1]}, f)

A = PrepareData()

