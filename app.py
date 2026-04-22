from flask import Flask, request, jsonify

app = Flask(__name__)

class DummyModel:
    def predict(self, X):
        # This simulates a model returning the sum of each row
        return [sum(row) for row in X]

# Initialize the model instance
MODEL = DummyModel()

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    X = data["X"]
    y = MODEL.predict(X)
    return jsonify({"y": y}), 200