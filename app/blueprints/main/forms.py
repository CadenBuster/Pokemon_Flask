from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired


class PokemonForm(FlaskForm):
    pokemon = StringField('Enter a Pokemon: ', validators=[DataRequired()])
    submit_btn = SubmitField('Get Info')

