from flask import Flask, render_template, request, redirect, url_for
import pickle

app = Flask(__name__)

with open('housing_price_pred_model.pkl', 'rb') as f:
    model = pickle.load(f)


@app.route('/')
def index():
    if request.method == "POST":
        pass
    else:
        return render_template('index.html')


@app.route('/predict', methods=['POST', 'GET'])
def predict():
    pass


if __name__ == "__main__":
    app.run(debug=True)
