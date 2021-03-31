"""Flask app for Cupcakes"""

from flask import Flask, request, jsonify, render_template, redirect
from models import db, connect_db, Cupcake
from forms import AddCupcake
import wtforms_json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "ZF2!Vt06BYQYgxKDU2of6O7hK"
wtforms_json.init()

connect_db(app)

@app.route("/")
def show_homepage():
    """ Show the homepage with client controls. """

    form = AddCupcake()
    
    return render_template("index.html", form=form)

############################## API ROUTES ##############################

@app.route("/api/cupcakes")
def get_all_cupcakes():
    """ Get and return all Cupcakes. """

    all_cupcakes = [c.serialize() for c in Cupcake.query.all()]

    return jsonify(cupcakes=all_cupcakes)

@app.route("/api/cupcakes/<int:cupcake_id>")
def get_cupcake(cupcake_id):
    """ Get and return a Cupcake by id. """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    return jsonify(cupcake=cupcake.serialize())

@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """ Create and return a new Cupcake. """
    
    form = AddCupcake.from_json(request.json)

    if form.validate_on_submit():
        new_cupcake = Cupcake(
            flavor=form.flavor.data,
            size=form.size.data,
            rating=form.rating.data,
            image=form.image.data or None
        )

        db.session.add(new_cupcake)
        db.session.commit()
        return redirect("/")

    else:
        new_cupcake = Cupcake(
            flavor=request.json["flavor"],
            size=request.json["size"],
            rating=request.json["rating"],
            image=request.json.get("image", None))

        db.session.add(new_cupcake)
        db.session.commit()

        return (jsonify(cupcake=new_cupcake.serialize()), 201)

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    """ Update and return a Cupcake by id. """

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor = request.json.get("flavor", cupcake.flavor)
    cupcake.size = request.json.get("size", cupcake.size)
    cupcake.rating = request.json.get("rating", cupcake.rating)
    cupcake.image = request.json.get("image", cupcake.image)
    db.session.commit()

    return jsonify(cupcake=cupcake.serialize())

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """ Delete a Cupcake by id and return confirmation message. """

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="deleted")

