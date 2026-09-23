from flask import Flask, render_template, request


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():

    latitude = None
    longitude = None

    if request.method == "POST":

        latitude = request.form["latitude"]
        longitude = request.form["longitude"]

        print("Latitude:", latitude)
        print("Longitude:", longitude)

    return render_template(
        "index.html",
        latitude=latitude,
        longitude=longitude
    )


if __name__ == "__main__":

    app.run(
        debug=True
    )