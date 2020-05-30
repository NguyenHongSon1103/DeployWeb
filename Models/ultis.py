import cv2
import base64
import numpy as np


def encode_np_array(image):
    ''' images: list of RGB images '''
    success, encoded_image = cv2.imencode('.jpg', image[:, :, ::-1])
    byte_image = encoded_image.tobytes()
    b64_string_image = base64.b64encode(byte_image).decode()
    return b64_string_image


# Tranfer bytes to image:
def read_image(img_bytes):
    return cv2.imdecode(np.asarray(bytearray(base64.b64decode(img_bytes)), dtype="uint8"), cv2.IMREAD_COLOR)
