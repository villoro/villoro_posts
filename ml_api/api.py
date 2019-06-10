""" Flask API """

from flask import Flask

from utils import read_model


APP = Flask("ML_API")

CLF = read_model()


@APP.route("/ping")
def ping():
    return "API working"


@APP.route("/", methods=["POST"])
def index():
    return "Hello, World!"


if __name__ == "__main__":
    APP.run(debug=True)
