from flask import Flask, request, jsonify, render_template
import os

import joblib

import pandas as pd

app = Flask(__name__)

MODEL_PATH = os.path.join(os.path.dirname(__file__), "lr_smote_pipeline.pkl")

MODEL = joblib.load(MODEL_PATH)

# The 11 raw features the model was trained on (train_cleaned.csv minus id/fake)
FEATURE_COLUMNS = [
    "profile pic",
    "nums/length username",
    "fullname words",
    "nums/length fullname",
    "name==username",
    "description length",
    "external URL",
    "private",
    "#posts",
    "#followers",
    "#follows",
]



class DummyModel:
    def predict(self, X):
        # This simulates a model returning the sum of each row
        return [sum(row) for row in X]

# Initialize the model instance
#MODEL = DummyModel()

@app.route("/", methods=["GET"])
def dashboard():
    return render_template("dashboard.html")

@app.route("/predict", methods=["POST"])
def predict():

    """

    Predict whether an Instagram account is fake.

    Expected JSON:

    {

      "profile_pic": 1,

      "nums_length_username": 0.0,

      "fullname_words": 2,

      "nums_length_fullname": 0.0,

      "name_eq_username": 0,

      "description_length": 45,

      "external_url": 1,

      "private": 0,

      "posts": 120,

      "followers": 850,

      "follows": 300

    }

    """

    data = request.get_json(force=True)

    if data is None:

        return jsonify({"error": "Request body must be JSON"}), 400

    try:

        row = {

            "profile pic": float(data.get("profile_pic", data.get("profile pic", 0))),

            "nums/length username": float(data.get("nums_length_username", data.get("nums/length username", 0))),

            "fullname words": float(data.get("fullname_words", data.get("fullname words", 0))),

            "nums/length fullname": float(data.get("nums_length_fullname", data.get("nums/length fullname", 0))),

            "name==username": float(data.get("name_eq_username", data.get("name==username", 0))),

            "description length": float(data.get("description_length", data.get("description length", 0))),

            "external URL": float(data.get("external_url", data.get("external URL", 0))),

            "private": float(data.get("private", 0)),

            "#posts": float(data.get("posts", data.get("#posts", 0))),

            "#followers": float(data.get("followers", data.get("#followers", 0))),

            "#follows": float(data.get("follows", data.get("#follows", 0))),

        }

        X = pd.DataFrame([row], columns=FEATURE_COLUMNS)

        prediction = int(MODEL.predict(X)[0])

        try:

            prob_fake = round(float(MODEL.predict_proba(X)[0][1]), 4)

        except AttributeError:

            prob_fake = None

        return jsonify({

            "prediction": prediction,

            "label": "fake" if prediction == 1 else "real",

            "probability_fake": prob_fake,

        }), 200

    except Exception as e:

        return jsonify({"error": str(e)}), 500
    

if __name__ == "__main__":
    app.run(debug=True)