from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable = False)
    password = db.Column(db.String)
    created_on = db.Column(db.DateTime, default = datetime.utcnow())
    games = db.relationship('Game', backref='host', lazy = 'dynamic')
    
    def hash_password(self, signup_password):
        return generate_password_hash(signup_password)
    
    def from_dict(self, user_data):
        self.first_name = user_data['first_name']
        self.last_name = user_data ['last_name']
        self.email = user_data['email']
        self.password = self.hash_password(user_data['password'])

game_participants = db.Table(
    'game_participants',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'))
)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    indoor = db.Column(db.String)
    score = db.Column(db.String)
    amount = db.Column(db.String)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    participants = db.relationship('User',
        secondary = game_participants,
        backref = 'game_participants',
        lazy = 'dynamic'
    )

    def from_dict(self, game_data):
        self.indoor = game_data['indoor']
        self.score = game_data ['score']
        self.amount = game_data['amount']
        self.user_id = game_data['user_id']

@login_manager.user_loader
def load_uer(user_id):
    return User.query.get(user_id)