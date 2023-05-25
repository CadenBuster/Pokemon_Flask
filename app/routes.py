from flask import request, render_template
import requests
from app import app
from .forms import LoginForm, PokemonForm, SignupForm

@app.route('/')
def home():
    return render_template('home.html')

USERS = {}

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        if email in USERS and password == USERS[email]['password']:
            return f"Hello, {USERS[email]['name']}"
        else:
            return 'Invalid email or password'
    else:
        return render_template('login.html',form = form)
    
@app.route('/signup', methods = ['GET','POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST' and form.validate_on_submit():
        name = form.first_name.data + ' ' + form.last_name.data
        email = form.email.data.lower()
        password = form.password.data
        USERS[email] = {
            'name' : name,
            'password' : password
        }
        return 'Thank you for signing up!'
    else:
        return render_template('signup.html', form = form)

@app.route('/getpokemon', methods =['GET','POST'])
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