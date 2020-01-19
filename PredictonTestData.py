import os
from tkinter.filedialog import askopenfilename as ask
from tkinter.filedialog import askopenfilenames as asks
import geopandas as gpd
import numpy as np
from cv2 import cv2
import json
import tensorflow as tf
os.environ['OPENCV_IO_MAX_IMAGE_PIXELS']=str(2**64)


class Predict():
    def __init__(self):
        self.shapepath = ask(title = "Import Shapefile")
        imagepaths = asks(title = "Import Image", filetypes=[("Image Files", "*.jpg")])
        graphname = ask(title = "Import Model File")
        labelsname = ask(title = "Import Labels File")
        self.Images = []
        for pth in imagepaths:
            self.Images.append(cv2.imread(pth, cv2.IMREAD_COLOR))
        print(len(self.Images))
        self.shape = gpd.read_file(self.shapepath)
        self.graph_def = tf.compat.v1.GraphDef()
        self.labels = []
        # Import the TF graph
        with tf.io.gfile.GFile(graphname, 'rb') as f:
            self.graph_def.ParseFromString(f.read())
            tf.import_graph_def(self.graph_def, name='')
        # Create a list of labels.
        with open(labelsname, 'rt') as lf:
            for l in lf:
                self.labels.append(l.strip())       
        # Get the input size of the model
        with tf.compat.v1.Session() as sess:
            input_tensor_shape = sess.graph.get_tensor_by_name('Placeholder:0').shape.as_list()
        self.network_input_size = input_tensor_shape[1]
        print("Network Input Size is "+ str(self.network_input_size))
        self.sizeControl()
        self.sizeAdjustment()
        self.predictionPhase()
        self.accuracy()
    def sizeControl(self):
        self.blank_image = np.zeros((self.network_input_size,self.network_input_size,3))
        self.blank_image[:,0:self.network_input_size//2] = (255,0,0)      # (B, G, R)
        self.blank_image[:,self.network_input_size//2:self.network_input_size] = (0,255,0)
        for i in range(len(self.Images)):
            try:
                print("Shape of {}. image is proper.".format(i)+str(self.Images[i].shape))
            except AttributeError:
                self.Images[i] = self.blank_image
                print("{}. image had bad shape. Corrected.".format(i))
    def sizeAdjustment(self):
        self.inputImages = []
        for image in self.Images:
            self.inputImages.append(cv2.resize(image, (self.network_input_size,self.network_input_size)))
        print(self.inputImages[-1].shape)
    def predictionPhase(self):
        output_layer = 'loss:0'
        input_node = 'Placeholder:0'
        self.outputs = []
        with tf.compat.v1.Session() as sess:
            for image in self.inputImages:
                try:
                    prob_tensor = sess.graph.get_tensor_by_name(output_layer)
                    predictions, = sess.run(prob_tensor, {input_node: [image] })
                except KeyError:
                    print ("Couldn't find classification output layer: " + output_layer + ".")
                    print ("Verify this a model exported from an Object Detection project.")
                    exit(-1)
                highest_probability_index = np.argmax(predictions)
                self.outputs.append(self.labels[highest_probability_index])
        self.shape['Roof_Types'] = self.outputs
        self.shape.to_file(self.shapepath)
    def accuracy(self):
        counter = 0
        for i in range(len(self.shape)):
            if self.shape.Roof_Types[i] == self.shape.Desired[i]:
                counter = counter + 1
        print("Test accuracy is {}.".format(counter/len(self.shape)))
A = Predict()