from keras import models
import numpy as np
import cv2
import tensorflow as tf
from Models.SSD_Mobilenetv2.detect import Detector


def load_names():
    with open('Models/CatBreeds/labels-breed.txt', 'r',encoding="UTF-8") as f:
        lines = f.readlines()
    # 0, 31, 36 is content
    breeds = [lines[i][:-1] for i in range(1, 31)]
    ages = [lines[i][-1] for i in range(32, 36)]
    genders = [lines[i][-1] for i in range(37, 39)]
    return breeds, ages, genders


class CatBreedModel:
    def __init__(self):
        self.__model__ = models.load_model(r'Models/CatBreeds/mobiletnet_model.h5',compile=False)
        self._detect_model_ = Detector()
        self.__model__._make_predict_function()
        self.__graph__ = tf.get_default_graph()
        self.__breeds__, self.__ages__, self.__genders__ = load_names()

    def predict(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        boxes = self._detect_model_.detect(image)
        if len(boxes) == 0:
            print("Cannot find any cat !")
            return None, None, None, None
        inputs = []
        for box in boxes:
            x1, y1, x2, y2 = box
            img = image[y1:y2, x1:x2] #Chỗ này có vấn đề gì đó ?
            img = cv2.resize(img, (224,224))
            img /= 255.0
            inputs.append(img)
        with self.__graph__.as_default():
            predictions = self.__model__.predict(image)

        breeds, ages, genders = [], [], []
        for pred in predictions:
            breeds.append(self.__breeds__[int(np.argmax(pred[0]))])
            ages.append(self.__ages__[int(np.argmax(pred[1]))])
            genders.append(self.__genders__[int(np.argmax(pred[2]))])
        return inputs, breeds, ages, genders




