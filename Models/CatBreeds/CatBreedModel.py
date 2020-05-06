from keras import models
import numpy as np
import cv2


class CatBreedModel:
    def __init__(self, path, size):
        self.model = models.load_model(path)
        self.size = size

    def predict(self, image):
        image = cv2.resize(image, self.size)
        image /= 255.0



