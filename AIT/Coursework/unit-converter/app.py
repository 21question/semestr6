from flask import Flask, render_template, request

app = Flask(__name__)


UNITS = {
    "length": {
        "meter": 1,
        "kilometer": 1000,
        "centimeter": 0.01,
        "millimeter": 0.001,
        "mile": 1609.34
    },

    "mass": {
        "kilogram": 1,
        "gram": 0.001,
        "pound": 0.453592,
        "ton": 1000
    },

    "time": {
        "second": 1,
        "minute": 60,
        "hour": 3600,
        "day": 86400
    },

    "volume": {
        "liter": 1,
        "milliliter": 0.001,
        "cubic_meter": 1000
    }
}


def convert(category, value, from_unit, to_unit):
    base_value = value * UNITS[category][from_unit]
    result = base_value / UNITS[category][to_unit]
    return round(result, 6)


@app.route("/", methods=["GET", "POST"])
def index():

    result = None

    category = "length"

    if request.method == "POST":

        category = request.form["category"]

        value = float(request.form["value"])

        from_unit = request.form["from_unit"]

        to_unit = request.form["to_unit"]

        result = convert(
            category,
            value,
            from_unit,
            to_unit
        )

    return render_template(
        "index.html",
        units=UNITS,
        result=result,
        selected_category=category
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )