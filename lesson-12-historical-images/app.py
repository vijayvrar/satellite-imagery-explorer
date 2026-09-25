from flask import Flask, render_template, request

from eo import create_historical_images


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():

    historical = None
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
                "Generating historical images:"
            )

            print(
                "Latitude:",
                latitude
            )

            print(
                "Longitude:",
                longitude
            )

            historical = create_historical_images(
                latitude,
                longitude
            )

            print(
                "2018 image created"
            )

            print(
                "2026 image created"
            )

        except Exception as e:

            error = str(e)

            print(
                "ERROR:",
                error
            )

    return render_template(
        "index.html",
        historical=historical,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)