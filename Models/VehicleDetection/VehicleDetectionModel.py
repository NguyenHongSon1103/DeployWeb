import cv2
import numpy as np
import time


class SSD_Detector:
    def __init__(self, size=None, conf=0.6):
        import tensorflow as tf
        self.labelIDs = {2: 'bicycle', 3: 'car', 6: 'bus', 4: 'bike', 8: 'truck'}
        self.conf = conf
        self.size = size
        self.tensor_dict = {'detection_boxes': 'detection_boxes:0',
                            'detection_scores': 'detection_scores:0', 'detection_classes': 'detection_classes:0'}
        pb_path = r'Models/SSD_Mobilenetv2/frozen_inference_graph.pb'

        with tf.gfile.GFile(pb_path, 'rb') as fid:
            od_graph_def = tf.GraphDef()
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')
        self.detection_graph = tf.get_default_graph()
        self.sess = tf.Session(graph=self.detection_graph)

    def __run_inference_for_single_image(self, image, sess):
        image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
        # Run inference
        output_dict = sess.run(self.tensor_dict,
                               feed_dict={image_tensor: image})

        # all outputs are float32 numpy arrays, so convert types as appropriate
        output_dict['detection_classes'] = output_dict['detection_classes'][0].astype(np.int64)
        output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
        output_dict['detection_scores'] = output_dict['detection_scores'][0]

        boxes = []
        labels = []
        scores = []
        for i, score in enumerate(output_dict['detection_scores']):
            id = output_dict['detection_classes'][i]
            if score > self.conf and id in [2, 3, 4, 6, 8]:
                boxes.append(output_dict['detection_boxes'][i])
                labels.append(self.labelIDs[id])
                scores.append(score)

        return boxes, labels, scores

    def __process_image(self, image):
        assert image is not None, "Image is none, check your read image steps"
        image_ = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        if self.size is not None:
            image_ = cv2.resize(image, self.size)
        tensor_in = image_ / 255.0
        tensor_in = np.expand_dims(image_, 0)
        return tensor_in

    def detect(self, image):
        """
        :param image: BGR mode
        :return: RGB bounding box of object
        """
        tensor_in = self.__process_image(image)
        boxes, labels, scores = self.__run_inference_for_single_image(tensor_in, self.sess)
        crops = []
        h, w = image.shape[:2]
        for box in boxes:
            y1, x1, y2, x2 = int(box[0] * h), int(box[1] * w), int(box[2] * h), int(box[3] * w)
            img = image[y1:y2, x1:x2]
            img = cv2.resize(img, (224, 224))
            crops.append(img)

        return crops, labels, scores


class YoloV3_Detector():
    def __init__(self, img_size=(416, 416), mode='tiny', iou_thres=0.6):
        self.img_size = img_size  # (320, 192) or (416, 256) or (608, 352) for (height, width)
        if mode == 'full':
            weights = 'Models/VehicleDetection/UltraYolov3/weights/yolov3spp-ultralytics.weights'
            cfg = 'Models/VehicleDetection/UltraYolov3/cfg/yolov3-spp.cfg'
            self.custom_conf = 0.4
        elif mode == 'tiny':
            weights = 'Models/VehicleDetection/UltraYolov3/weights/yolov3-tiny-ultralystic.weights'
            cfg = 'Models/VehicleDetection/UltraYolov3/cfg/yolov3-tiny.cfg'
            self.custom_conf = 0.1
        else:
            print("mode only 'full' or 'tiny' option")
            return
        self.iou_thres = iou_thres
        self.LABEL_IDS = [1, 2, 3, 5]
        self.classes = {2: 'car', 3: 'bike', 5: 'bus', 1: 'bicycle'}
        self.net = cv2.dnn.readNetFromDarknet(cfg, weights)
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_OPENCL_FP16)
        # Get the output layer from YOLO
        layers = self.net.getLayerNames()
        self.output_layers = [layers[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

    def detect(self, image):
        height, width = image.shape[:2]
        blob = cv2.dnn.blobFromImage(image, 1/255.0, self.img_size, swapRB=True, crop=False)  # very fast

        e1 = time.time()
        self.net.setInput(blob)
        layer_outputs = self.net.forward(self.output_layers)  # too slow
        # layer_outputs = yolo_model.predict(blob) # a list contain 3 array shape (1,19,19,27) , (1,38,38,27) , (1 ,76, 76 ,27)

        _labels, confidences, b_boxes = [], [], []

        for output in layer_outputs:
            for detection in output:
                _scores = detection[5:]
                class_id = int(np.argmax(_scores))
                confidence = _scores[class_id]
                if(confidence > self.custom_conf) and (class_id in self.LABEL_IDS):
                    center_x, center_y, w, h = (detection[0:4] * np.array([width, height, width, height])).astype('int')

                    xmin, xmax = int(center_x - w / 2), int(center_x + w / 2)
                    ymin, ymax = int(center_y - h / 2), int(center_y + w / 2)

                    b_boxes.append([xmin, ymin, xmax, ymax])
                    confidences.append(float(confidence))
                    _labels.append(self.classes[class_id])

        # Perform non maximum suppression for the bounding boxes to filter overlapping and low confident bounding boxes
        indices = cv2.dnn.NMSBoxes(b_boxes, confidences, self.custom_conf, self.iou_thres)
        if len(indices) == 0:
            return [], [], []
        crops, labels, scores = [], [], []
        for indice in indices.flatten():
            x1, y1, x2, y2 = b_boxes[indice]
            crops.append(image[y1:y2, x1:x2])
            labels.append(_labels[indice])
            scores.append(confidences[indice])

        return crops, labels, scores




