from flask import Flask, jsonify, render_template, request
from query import (
    get_random_cafe,
    get_all_cafe,
    get_cafe_by_location,
    add_new_cafe,
    update_cafe_price,
    report_closed
)
from query import Cafe


app = Flask(__name__)

##Connect to Database


##Cafe TABLE Configuration


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/random")
def random_cafe():
    """
    Endpoint to fetch a randomly selected Cafe
    Returns:
      JSON response with randomly selected cafe details
    """
    random_cafe = get_random_cafe()
    return jsonify(random_cafe)


@app.route("/all")
def all_cafe():
    """
    Endpoint to fetch all the Cafe's in the database
    Returns:
        JSON response with all cafes
    """
    all = get_all_cafe()
    return jsonify(all)


@app.route("/cafe")
def cafe_by_location():
    """
    Endpoint to fetch a cafe by location
    Returns:
        JSON response with cafes in the specified location
    """
    location = request.args.get("location")
    if not location:
        return jsonify({"error": "location parameter is required"})
    cafes = get_cafe_by_location(location)
    if not cafes:
        return jsonify({"error": "No cafes found for the specified location"}), 404
    return jsonify(cafes)


@app.route("/add", methods=["POST"])
def add_cafe():
    """
    Endpoint to add  a new cafe to the database
    Returns:
        JSON response with the newly added cafe details
    """
    formdata = request.form
    new_cafe = add_new_cafe(formdata)
    return jsonify(new_cafe)


@app.route("/update_price/<int:cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    """
    Endpoint to update the price of an existing cafe
    Args:
      cafe_id (int): ID of the cafe to be updated
    """
    new_price = request.args.get("new_price")
    if not new_price:
        return jsonify({"error": "new price parameter is missing"})
    response = update_cafe_price(new_price, cafe_id)
    if "Cafe with id" in response:
        return jsonify(response), 404
    elif response == "failed":
        return jsonify({"error": "Failed to update cafe price"}), 500
    else:
        return jsonify({"message": "Cafe price updated successfully"})


@app.route("/report_closed/<int:cafe_id>", methods=["DELETE"])
def close(cafe_id):
    """
    Endpoint to report a cafe as closed
    Args:
      cafe_id(int): ID of the cafe to be reported as closed
    Returns:
      JSON response with success or failure message
    """
    response = report_closed(cafe_id)
    if response == "success":
        return jsonify({"message": "Cafe reported as closed successfully"})
    else:
        return jsonify({"error": response}), 404


## HTTP GET - Read Record

## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == "__main__":
    app.run(debug=True)
