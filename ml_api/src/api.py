""" Flask API """

from flask import jsonify, Flask, request

import preprocess as prep
from utils import read_model


APP = Flask("ML_API")

CLF = read_model()


def create_response(code, message, results=None):
    """ Creates and html response """

    data = {"status": int(code), "description": message}

    if results is not None:
        data["results"] = results

    response = jsonify(data)
    response.status_code = int(code)

    return response


@APP.route("/ping")
def ping():
    """ Test that the API is working """
    return "API working"


@APP.route("/", methods=["POST"])
def predict():
    """ Predict using the classifier """

    data = request.json

    print(data)

    if data.get("token", None) != "aaaa":
        return create_response(401, "Bad token")

    if "data" not in data:
        return create_response(400, "Missing data in request")

    df = prep.create_dataframe_from_json(data["data"])

    if df is None:
        return create_response(400, f"Data should have {prep.FEATURES_ORIGIN}")

    df = prep.preprocess(df)
    predictions = CLF.predict(df)

    return create_response(200, "Predictions done", predictions)


if __name__ == "__main__":
    APP.run(debug=True)
