from flask import Flask, render_template, request, redirect, url_for
import pickle
from sklearn.preprocessing import OneHotEncoder
import pandas as pd

app = Flask(__name__)

with open('housing_price_pred_model.pkl', 'rb') as f:
    model = pickle.load(f)

encoder = OneHotEncoder(categories=[['rural', 'suburb', 'urban']])
encoder.fit([['rural'], ['suburb'], ['urban']])
feature_names = ['SquareFeet', 'Bedrooms', 'Bathrooms', 'YearBuilt', 'Neighborhood_Rural', 'Neighborhood_Suburb', 'Neighborhood_Urban']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST', 'GET'])
def predict():
    if request.method == "POST":
        try:
            square_feet = int(request.form['square_feet'])
            bedrooms = int(request.form['bedrooms'])
            bathrooms = int(request.form['bathrooms'])
            neighborhood = request.form['neighborhood']
            year = int(request.form['year'])
        except ValueError:
            return 'Invalid input. Please enter numerical values for square feet, bedrooms, bathrooms, and year.'

        neighborhood_encoded = encoder.transform([[neighborhood]])

        data = {
            'SquareFeet': [square_feet],
            'Bedrooms': [bedrooms],
            'Bathrooms': [bathrooms],
            'YearBuilt': [year],
            'Neighborhood_Rural': neighborhood_encoded[0, 0],
            'Neighborhood_Suburb': neighborhood_encoded[0, 1],
            'Neighborhood_Urban': neighborhood_encoded[0, 2]
        }
        df = pd.DataFrame(data, columns=feature_names)

        prediction = model.predict(df)
        prediction = round(prediction[0], 3)

        return render_template('prediction.html', square_feet= square_feet, bedrooms= bedrooms, bathrooms= bathrooms, neighborhood= neighborhood, year= year, prediction= prediction)

    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
