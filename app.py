from flask import Flask
from flask import render_template, request, Response, json
from Models.CommentSemantic import CommentSemantic
from Models import ultis

SERVER_NAME = 'http://localhost:5000'
app = Flask(__name__)


CSModel = CommentSemantic.CommentSemantic(ultis.encode_model_path, ultis.model_path)


@app.route("/runCommentSemantic", methods=['POST'])
def runCommentSemantic():
    comment = request.form['comment']
    prediction = CSModel.predict(comment)
    respond_dict = dict()
    if prediction is None:
        respond_dict['prediction'] = -1
    else:
        prediction = prediction[0]
        respond_dict['prediction'] = prediction
    return Response(json.dumps(respond_dict), status=201)


# @app.route("/commentSemantic/view",methods=["GET"])
# def view():
#     return render_template("classifyFace.html")


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