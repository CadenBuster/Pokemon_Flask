from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash

pokemon_caught = db.Table(
    'pokemon_caught',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('poke_id', db.Integer, db.ForeignKey('pokemon.id'))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable = False)
    password = db.Column(db.String)
    created_on = db.Column(db.DateTime, default = datetime.utcnow())
    caught = db.relationship('Pokemon',
        secondary = pokemon_caught,
        backref= 'pokemon_caught',
        lazy='dynamic'                      
    )
    
    def hash_password(self, signup_password):
        return generate_password_hash(signup_password)
    
    def from_dict(self, user_data):
        self.first_name = user_data['first_name']
        self.last_name = user_data ['last_name']
        self.email = user_data['email']
        self.password = self.hash_password(user_data['password'])


class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    img_url = db.Column(db.String)
    ability = db.Column(db.String)
    base_xp = db.Column(db.String)
    

    def from_dict(self,poke_data):
        self.name = poke_data['name']
        self.img_url = poke_data['sprite']
        self.ability = poke_data['ability']
        self.base_xp = poke_data['base_xp']
    
    def check(pokename):
        return Pokemon.query.filter_by(name=pokename).first()

@login_manager.user_loader
def load_uer(user_id):
    return User.query.get(user_id)