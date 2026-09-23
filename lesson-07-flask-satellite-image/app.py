from flask import Flask, render_template
from eo import create_rgb_image


app = Flask(__name__)


@app.route("/")
def home():

    latitude = 13.0827
    longitude = 80.2707

    result = create_rgb_image(
        latitude,
        longitude
    )

    return render_template(
        "index.html",
        result=result
    )


if __name__ == "__main__":

    app.run(
        debug=True
    )