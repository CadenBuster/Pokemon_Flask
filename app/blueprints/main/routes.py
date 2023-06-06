from flask import request, render_template, redirect, url_for, flash
import requests
from . import main
from app import db
from app.blueprints.main.forms import PokemonForm
from flask_login import current_user, login_required
from app.models import Pokemon, User

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
            
            if not Pokemon.check(pokemon_data['name']):
                pokemon = Pokemon()
                pokemon.from_dict(pokemon_data)
                db.session.add(pokemon)
                db.session.commit()

            return render_template('forms.html',pokemon_data = pokemon_data, pokeform = pokeform)
        else:
            print('Invalid name')
    return render_template('forms.html', pokeform = pokeform)


@main.route('/catch/<string:poke_name>')
@login_required
def catch(poke_name):
    poke = Pokemon.query.filter_by(name=poke_name).first()
    if poke:
        if poke not in current_user.caught:
            if len(current_user.caught.all()) < 5:
                current_user.caught.append(poke)
                db.session.commit()
                flash(f'Successfully caught {poke.name}')
                return redirect(url_for('main.team'))
            else:
                flash('You can only have five pokemon on your team!')
                return redirect(url_for('main.team'))
        else:
            flash(f'You can only have one {poke.name} on your team')
            return redirect(url_for('main.team'))
    else:
        flash('That Pokemon does not exist!')
        return redirect(url_for('main.team'))

@main.route('/release/<int:poke_id>')
@login_required
def release(poke_id):
    poke = Pokemon.query.get(poke_id)
    if poke:
        current_user.caught.remove(poke)
        db.session.commit()
        flash(f'{poke.name} has been released.')
        return redirect(url_for('main.team'))
    else:
        flash('You can only release Pokemon that are on your team.')
        return redirect(url_for(main.team))


@main.route('/team')
@login_required
def team():
    team = current_user.caught.all()
    return render_template('poketeam.html', team = team)

@main.route('/trainers')
@login_required
def trainer():
    trainers = User.query.all()
    return render_template('trainer.html', trainers=trainers)

@main.route('/battle/<int:defender>')
@login_required
def battle(defender):
    attacker = current_user
    defender = User.query.get(defender)
    attacker_stats = 0
    defender_stats = 0
    for pokemon in attacker.caught.all():
        attacker_stats += int(pokemon.base_xp)

    for pokemon2 in defender.caught.all():
        defender_stats += int(pokemon2.base_xp)

    if attacker_stats > defender_stats:
        flash(f'{attacker.first_name} wins!')
        return render_template('trainer.html')
    elif attacker_stats == defender_stats:
        flash(f'Tie!')
        return render_template('trainer.html')
    else:
        flash(f'{defender.first_name} defeated you!')
        return render_template('trainer.html')
