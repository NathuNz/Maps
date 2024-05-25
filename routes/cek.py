import numpy as np
from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)

# Load the machine learning model
with open('elm_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json  # Get input data from request
    prediction = model.predict(data)  # Make predictions using the model
    return jsonify({'prediction': prediction.tolist()})  # Return predictions

if __name__ == '__main__':
    app.run(debug=True)