from flask import Flask, jsonify, request
from flask_cors import CORS
from handlers import roothandler, feedshandler, sourcehandler
from feedparser import helper as fch

app = Flask(__name__)
CORS(app)

fch.getData()


@app.route('/', methods=['GET'])
def root():
    return roothandler()


@app.route('/<string:rt>', methods=['GET'])
def apiroute(rt):
    if request.method == 'GET':
        if rt.strip() == "feed":
            return feedshandler()
        elif rt.strip() in fch.configs['sources'].keys():
            return sourcehandler(rt)
        else:
            return jsonify({'error': 'Bad request'}), 400


if __name__ == '__main__':
    app.run()
