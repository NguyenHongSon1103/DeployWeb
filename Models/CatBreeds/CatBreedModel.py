from keras import models
import numpy as np
import cv2
import tensorflow as tf
from Models.SSD_Mobilenetv2.detect_cat import Detector


def load_names():
    with open('Models/CatBreeds/labels-breed.txt', 'r',encoding="UTF-8") as f:
        lines = f.readlines()
    lines = [line[:-1] for line in lines]
    breeds = [lines[i] for i in range(1, 31)]
    ages = [lines[i] for i in range(32, 36)]
    genders = [lines[i] for i in range(37, 39)]
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
        h, w = image.shape[:2]
        boxes = self._detect_model_.detect(image)
        if len(boxes) == 0:
            print("Cannot find any cat !")
            return None, None, None, None
        inputs = []
        crops = []
        for i, box in enumerate(boxes):
            y1, x1, y2, x2 = int(box[0]*h), int(box[1]*w),int(box[2]*h), int(box[3]*w)
            img = image[y1:y2, x1:x2]
            img = cv2.resize(img, (224,224))
            crops.append(img)
            img = np.array(img, dtype=float) / 255.0
            inputs.append(img)
        inputs = np.array(inputs)
        with self.__graph__.as_default():
            predictions = self.__model__.predict(inputs)
        breeds, ages, genders = [], [], []
        breeds_out, ages_out, genders_out = predictions
        for breed_out, age_out, gender_out in zip(breeds_out, ages_out, genders_out):
            breeds.append(self.__breeds__[int(np.argmax(breed_out))])
            ages.append(self.__ages__[int(np.argmax(age_out))])
            genders.append(self.__genders__[int(np.argmax(gender_out))])
        return crops, breeds, ages, genders




