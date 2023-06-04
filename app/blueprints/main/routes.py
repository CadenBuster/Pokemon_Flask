from flask import request, render_template, redirect, url_for, flash
import requests
from . import main
from app import db
from app.blueprints.main.forms import PokemonForm
from flask_login import current_user, login_required
from app.models import Pokemon

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/getpokemon', methods =['GET','POST'])
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


@main.route('/catch/<int:poke_id>')
@login_required
def catch(poke_id):
    poke = Pokemon.query.get(poke_id)
    if poke:
        current_user.followed.append(poke)
        db.session.commit()
        flash(f'Successfully caught {poke.name}')
        return redirect(url_for('main.team'))
    else:
        flash('That Pokemon does not exist!')
        return redirect(url_for('main.team'))