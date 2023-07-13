from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash


user_following = db.Table(
    'user_following',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    user_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable = False)
    password = db.Column(db.String)
    points = db.Column(db.Integer, nullable=False)
    rebounds = db.Column(db.Integer, nullable = False)
    assists = db.Column(db.Integer, nullable = False)
    games_played = db.Column(db.Integer, nullable = False)
    triple_double = db.Column(db.String, nullable = False)
    sus = db.Column(db.String, nullable=False)
    snell = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, default = datetime.utcnow())
    followed = db.relationship('User',
        secondary = user_following,
        primaryjoin = (user_following.columns.follower_id == id),
        secondaryjoin = (user_following.columns.followed_id == id),
        backref = db.backref('user_following', lazy='dynamic'),
        lazy = 'dynamic'
    )
    games = db.relationship('Game', backref='host', lazy = 'dynamic')
    
    
    def hash_password(self, signup_password):
        return generate_password_hash(signup_password)
    
    def from_stats(self, stat_data):
        self.points = stat_data['points']
        self.assists = stat_data['assists']
        self.rebounds = stat_data['rebounds']
        self.games_played = stat_data['games_played']
    
    def from_achieve(self,achievement_data):
        self.triple_double = achievement_data['triple_double']
        self.sus = achievement_data['sus']
        self.snell = achievement_data['snell']

    def from_dict(self, user_data):
        self.first_name = user_data['first_name']
        self.last_name = user_data ['last_name']
        self.user_name = user_data['user_name']
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
    open = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    lat = db.Column(db.Float)
    long = db.Column(db.Float)
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
        self.open = game_data['open']
        self.city = game_data['city']
        self.state = game_data['state']
        self.lat = game_data['lat']
        self.long = game_data['long']

@login_manager.user_loader
def load_uer(user_id):
    return User.query.get(user_id)