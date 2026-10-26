
# Import the libraries
import os
import joblib                       # to load the saved model
import pandas as pd                 # to create the input dataframe
from flask import Flask, request, jsonify

# Create the Flask app
extraalearn_api = Flask("ExtraaLearn")

# Load the saved model (the model file is kept in the same folder as this file)
model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "extraalearn_model.joblib")
model = joblib.load(model_path)

# The columns the model was trained on
FEATURES = [
    "age",
    "current_occupation",
    "first_interaction",
    "profile_completed",
    "website_visits",
    "time_spent_on_website",
    "page_views_per_visit",
    "last_activity",
    "print_media_type1",
    "print_media_type2",
    "digital_media",
    "educational_channels",
    "referral",
]


# Home page
@extraalearn_api.get("/")
def home():
    return "Welcome to the ExtraaLearn Lead Conversion Prediction API"


# Prediction endpoint for one lead
@extraalearn_api.post("/v1/predict")
def predict():
    # Get the JSON data sent by the user
    lead = request.get_json(silent=True)

    if lead is None:
        return jsonify({"error": "Please send the lead details as JSON"}), 400

    # Check that all the required fields are there
    missing = [col for col in FEATURES if col not in lead]
    if missing:
        return jsonify({"error": "Missing fields: " + ", ".join(missing)}), 400

    try:
        # Put the values in a dataframe in the same column order as training
        input_data = pd.DataFrame([{col: lead[col] for col in FEATURES}])

        # Predicted class and probability of conversion
        prediction = int(model.predict(input_data)[0])
        probability = float(model.predict_proba(input_data)[0][1])
    except Exception as e:
        return jsonify({"error": "Could not make a prediction: " + str(e)}), 400

    return jsonify({
        "prediction": prediction,
        "conversion_probability": round(probability, 4),
        "result": "Likely to convert" if prediction == 1 else "Unlikely to convert",
    })


# Run the app (only used when running this file directly, the Docker container uses gunicorn)
if __name__ == "__main__":
    extraalearn_api.run(debug=True)
