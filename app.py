from flask import Flask,request,app,jsonify,url_for,render_template
import pickle
import numpy as np
import pandas as pd


app = Flask(__name__)
#model = pickle.load(open(""))

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict_api',methods=['POST'])
def predict_api:
    data = request.json['data']
    print(data)




if __name__ =="__main__":
    app.run(debug=True)
