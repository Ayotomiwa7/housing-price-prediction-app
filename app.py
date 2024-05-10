from flask import Flask, render_template, request, redirect, url_for
import pickle
from sklearn.preprocessing import OneHotEncoder

app = Flask(__name__)

# Load the model and encoder
with open('housing_price_pred_model.pkl', 'rb') as f:
    model = pickle.load(f)

encoder = OneHotEncoder(categories=[['suburb', 'rural', 'urban']])


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST', 'GET'])
def predict():
    if request.method == "POST":
        square_feet = int(request.form['square_feet'])
        bedrooms = int(request.form['bedrooms'])
        bathrooms = int(request.form['bathrooms'])
        neighborhood = request.form['neighborhood']
        year = int(request.form['year'])

        encoder.fit([['suburb'], ['rural'], ['urban']])

        neighborhood_encoded = encoder.transform([[neighborhood]])

        prediction = model.predict([[square_feet, bedrooms, bathrooms, *neighborhood_encoded.toarray()[0], year]])

        return f"prediction: {prediction}"

    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
