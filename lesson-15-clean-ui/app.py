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

            historical = create_historical_images(
                latitude,
                longitude
            )

        except Exception as e:

            error = str(e)

            print("ERROR:", error)

    return render_template(
        "index.html",
        historical=historical,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)