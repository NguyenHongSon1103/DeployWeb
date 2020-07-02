from flask import Flask
from flask import render_template, request, Response, json
#from Models.CommentSemantic import CommentSemantic
#from Models.CatBreeds import CatBreedModel
from Models.VehicleDetection.VehicleDetectionModel import YoloV3_Detector
from Models import ultis
from time import time

SERVER_NAME = 'http://localhost:5000'
app = Flask(__name__)

#CSModel = CommentSemantic.CommentSemantic()
#CBModel = CatBreedModel.CatBreedModel()
VehicleDetector = YoloV3_Detector(img_size=(416,416), mode='full', iou_thres=0.5)


@app.route("/runCommentSemantic", methods=['POST'])
def runCommentSemantic():
    s = time()
    comment = request.form['comment']
    prediction, conf = CSModel.predict(comment, mode='svm')
    respond_dict = dict()
    if prediction is None:
        respond_dict['prediction'] = '-1'
    else:
        respond_dict['prediction'] = str(prediction)
        respond_dict['confidence'] = str(conf)
    e = time()
    respond_dict['exetime'] = "%.4f" % (e - s)
    return Response(json.dumps(respond_dict), status=201)


@app.route("/runBreedsCat", methods=["POST"])
def runBreedsCat():
    s = time()
    image = request.form['image'][23:]
    # print('ảnh: ', image)
    image = ultis.read_image(image)
    crops, breeds, ages, genders = CBModel.predict(image)
    response_dict = dict()
    if crops is None:
        response_dict['status'] = 'nocat'
    else:
        response_dict['status'] = 'cat'
        response_dict['count'] = len(crops)
        for i, crop in enumerate(crops):
            response_dict['prediction_' + str(i)] = {'box': ultis.encode_np_array(crop), 'breed': breeds[i],
                                                     'age': ages[i], 'gender': genders[i]}
    e = time()
    response_dict['exetime'] = '%.4f' % (e - s)
    return Response(json.dumps(response_dict), status=201)


@app.route('/vehicleDetection')
def vehicleDetection():
    return render_template("Product/VehicleDetection.html")


@app.route("/runVehicleDetection", methods=["POST"])
def runVehicleDetection():
    s = time()
    image = request.form['image'][23:]
    # print('ảnh: ', image)
    image = ultis.read_image(image)
    crops, labels, scores = VehicleDetector.detect(image)
    response_dict = dict()
    if len(crops) == 0:
        response_dict['status'] = 'novehicle'
    else:
        response_dict['status'] = 'vehicle'
        response_dict['count'] = len(crops)
        for i, crop in enumerate(crops):
            response_dict['prediction_' + str(i)] = {'box': ultis.encode_np_array(crop), 'label': labels[i],
                                                     'score': str(scores[i])}
    e = time()
    response_dict['exetime'] = '%.4f' % (e - s)
    return Response(json.dumps(response_dict), status=201)


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/commentSemantic')
def commentSemantic():
    return render_template("Product/CommentSemantic.html")


@app.route('/catBreed')
def catBreed():
    return render_template("Product/CatBreed.html")


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=3000)
