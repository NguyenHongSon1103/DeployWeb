import cv2
import numpy as np
import tensorflow as tf


class Detector:
    def __init__(self, filter_name, size=None, conf=0.6):
        self.filter_name = filter_name
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

        detection_graph = tf.get_default_graph()
        self.sess = tf.Session(graph=detection_graph)

    def __run_inference_for_single_image(self, image, sess):
        image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')
        # Run inference
        output_dict = sess.run(self.tensor_dict,
                               feed_dict={image_tensor: image})

        # all outputs are float32 numpy arrays, so convert types as appropriate
        output_dict['detection_classes'] = output_dict['detection_classes'][0].astype(np.int64)
        output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
        output_dict['detection_scores'] = output_dict['detection_scores'][0]

        boxes = []
        class_ids = []
        scores = []
        for i, score in enumerate(output_dict['detection_scores']):
            if score > self.conf:
                boxes.append(output_dict['detection_boxes'][i])
                class_ids.append(output_dict['detection_classes'][i])
                scores.append(output_dict['detection_scores'][i])

        return boxes, class_ids, scores

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
        boxes, _, _ = self.__run_inference_for_single_image(image, self.sess)
        return boxes
