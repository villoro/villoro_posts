""" Flask app index """

import oyaml as yaml

from markdown import markdown
from flask import Flask, render_template

APP = Flask(__name__)


def _read_yaml(filename):
    """ auxiliar function to raad a yaml """

    with open(f"src/content/{filename}.yaml", encoding="utf-8") as file:
        out = yaml.load(file)

    # Transform from makrdown to html
    if "description" in out:
        out["description"] = markdown(out["description"], extensions=["fenced_code", "codehilite"])

    return out


@APP.route("/")
@APP.route("/home.html")
def home():
    """ home page """

    return render_template("home.html", **_read_yaml("home"))


@APP.route("/about.html")
def about():
    """ about me page """

    return render_template("about.html", **_read_yaml("about"))


if __name__ == "__main__":
    APP.run(debug=True)
