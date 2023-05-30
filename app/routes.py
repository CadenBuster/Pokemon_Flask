from flask import request, render_template, redirect, url_for, flash
import requests
from app import app,db
from .forms import LoginForm, PokemonForm, SignupForm
from app.models import User
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user, login_required


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        queried_user = User.query.filter(User.email == email).first()
        if queried_user and check_password_hash(queried_user.password, password):
            login_user(queried_user)
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'error')
            return render_template('login.html',form = form)
    else:
        return render_template('login.html',form = form)
    
@app.route('/signup', methods = ['GET','POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST' and form.validate_on_submit():

        user_data = {
            'first_name' : form.first_name.data,
            'last_name' : form.last_name.data,
            'email' : form.email.data.lower(),
            'password' : form.password.data
        }

        new_user = User()

        new_user.from_dict(user_data)

        db.session.add(new_user)
        db.session.commit()


        flash('Thank you for signing up!', 'success')
        return redirect(url_for('login'))
    else:
        return render_template('signup.html', form = form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out!')
    return redirect(url_for('home'))

@app.route('/getpokemon', methods =['GET','POST'])
@login_required
def get_poke():
    pokeform = PokemonForm()
    if request.method == 'POST' and pokeform.validate_on_submit():
        pokemon = pokeform.pokemon.data.lower()
        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon}'
        response = requests.get(url)
        if response.ok:
            poke_data = response.json()
            pokemon_data = {
                'name' : poke_data['forms'][0]['name'],
                'base_xp' : poke_data['base_experience'],
                'ability' : poke_data['abilities'][0]['ability']['name'],
                'sprite' : poke_data['sprites']['front_default']
            }
            return render_template('card.html',pokemon_data = pokemon_data, pokeform = pokeform)
        else:
            print('Invalid name')
    return render_template('forms.html', pokeform = pokeform)