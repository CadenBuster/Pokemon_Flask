from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField
from wtforms.validators import DataRequired

class GameForm(FlaskForm):
    indoor = RadioField('Indoor/Outdoor', choices=[('Indoor','Indoor'),('Outdoor','Outdoor')], default = 'Indoor')
    score = RadioField('ScoreType', choices=[('1s and 2s','1s and 2s'),('2s and 3s','2s and 3s')],default = '1s and 2s')
    amount = RadioField('PlayerCount', choices=[('3 vs 3','3 vs 3'),('5 vs 5','5 vs 5')], default = '3 vs 3')
    submit_btn = SubmitField('Host Game')
