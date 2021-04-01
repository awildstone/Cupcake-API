"""Forms for Cupcakes. """

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField
from wtforms.validators import InputRequired, Optional, URL, NumberRange

FLAVORS = ["chocolate", "vanilla", "red velvet", "carrot", "pumpkin", "cherry"]
SIZES = [("Small", "SM"), ("Medium", "MD"), ("Large", "LG")]

class AddCupcake(FlaskForm):
    """ Add new Cupcake form. """

    flavor = SelectField("Flavor", choices=[(flavor, flavor) for flavor in FLAVORS], validators=[InputRequired(message="You must select the flavor of the Cupcake.")])
    size = SelectField("Size", choices=[*SIZES], validators=[InputRequired(message="You must enter the size of the Cupcake.")])
    rating = FloatField("Rating", validators=[NumberRange(min=1, max=10, message="You must enter an rating between 1-10"), InputRequired(message="You must enter your rating for the Cupcake.")])
    image = StringField("Image URL", validators=[URL(message="You must enter a valid URL"), Optional()]) 