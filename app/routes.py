from flask import request, render_template
import requests
from app import app
from forms import LoginForm

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        return '<p>Logged In</p>'
    else:
        return render_template('login.html',form = form)

@app.route('/getpokemon', methods =['GET','POST'])
def get_poke():
    if request.method == 'POST':
        pokemon = request.form.get('pokemon')
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
            return render_template('card.html', pokemon_data = pokemon_data)
        else:
            print('Invalid name')
    return render_template('forms.html')