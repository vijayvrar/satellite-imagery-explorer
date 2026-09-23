from flask import Flask, render_template, request

from eo import create_rgb_image


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():

    result = None
    error = None

    if request.method == "POST":

        try:

            latitude = float(
                request.form["latitude"]
            )

            longitude = float(
                request.form["longitude"]
            )

            print(
                "Received coordinates:",
                latitude,
                longitude
            )

            result = create_rgb_image(
                latitude,
                longitude
            )

        except Exception as e:

            error = str(e)

            print(
                "ERROR:",
                error
            )

    return render_template(
        "index.html",
        result=result,
        error=error
    )


if __name__ == "__main__":

    app.run(
        debug=True
    )