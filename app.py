from flask import Flask, render_template, request, redirect, url_for
import pickle

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    pass

if __name__ == "__main__":
    app.run(debug=True)