from flask import Flask
from flask import request
import numpy as np
import os
import cv2
from descriptor import Descriptor
from flask_pymongo import PyMongo
from scipy.spatial.distance import euclidean,cosine
from flask import jsonify
from flask_cors import CORS, cross_origin
import matplotlib.pyplot as plt

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'image'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/image'
app.config['UPLOAD_FOLDER'] = './'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

mongo = PyMongo(app)

path = "./data"

@app.route('/')
def process():
    dirs = os.listdir(path)
    features = mongo.db.features
    for file in dirs:
        # đọc từng file
       image = cv2.imread(path+'/'+file)
    #    Vẽ sơ đồ histogram của 3 đặc trưng : 
        # đặc trưng màu sắc, 
       color_feature = Descriptor.color_history(image,8)
        # đặc trưng kết cấu ảnh(lpb),
       lpb_feature = Descriptor.lpb_history(image,24,8)
        # đặc trưng HOG
       hog_feature = Descriptor.hog(image,10,2,9)

       feature = list(np.hstack([color_feature, lpb_feature, hog_feature]))
       id = features.insert_one({
           'path':path+'/'+file,
           'feature':feature
       })

    return 'done'

@app.route('/search', methods=['POST'])
@cross_origin()
def search():

    # Dữ liệu đầu vào
    file = request.files['file'] 
    file.save('./'+file.filename)


    features = mongo.db.features
    # Đọc ảnh input
    image = cv2.imread('./'+file.filename)

    color_feature = Descriptor.color_history(image,8)
    lpb_feature = Descriptor.lpb_history(image,24,8)
    hog_feature = Descriptor.hog(image,10,2,9)

    feature = np.hstack([color_feature, lpb_feature, hog_feature])
    db_features = features.find();
    results_euclidean = {}
    results_cosine = {}
    for db_feature in db_features:
        dist_euclidean = euclidean(np.asarray(db_feature['feature']),feature)
        results_euclidean[db_feature['path']] = dist_euclidean
        dist_cosine = cosine(np.asarray(db_feature['feature']),feature)
        results_cosine[db_feature['path']] = dist_cosine


    results_euclidean = sorted([(d, n) for n, d in results_euclidean.items()])
    results_cosine = sorted([(d, n) for n, d in results_cosine.items()])
    return jsonify({'result_euclidean':results_euclidean,'result_cosine':results_cosine})


if __name__ == '__main__':
    app.run()