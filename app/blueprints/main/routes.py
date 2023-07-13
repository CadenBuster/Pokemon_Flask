from flask import request, render_template, redirect, url_for, flash
import requests
from . import main
from app import db
from flask_login import current_user, login_required
from app.models import User, Game
from app.blueprints.main.forms import GameForm, StatForm, SearchForm

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/games', methods = ['GET','POST'])
@login_required
def game():
    form = GameForm()
    if request.method == 'POST' and form.validate_on_submit():

        city = form.city.data.title()
        state = form.state.data.title()
        url = "https://geocoding-by-api-ninjas.p.rapidapi.com/v1/geocoding"
        querystring = {"city":city,"state":state,"country":"US"}
        headers={
            "X-RapidAPI-Key": "8e272dcadfmshca0c0e19694e049p12ab77jsn1c11e67b2682",
	        "X-RapidAPI-Host": "geocoding-by-api-ninjas.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers, params=querystring)
        if response.ok:
            location_data= response.json()
            print(location_data)
            for index in location_data:
                if index['state'] == state:
                    game_data = {
                        'city': city,
                        'state': state,
                        'indoor': form.indoor.data,
                        'score': form.score.data,
                        'amount': form.amount.data,
                        'open': 'open',
                        'user_id': current_user.id,
                        'lat': index['latitude'],
                        'long': index['longitude'],
                    }
                    new_game = Game()
                    new_game.from_dict(game_data)
                    db.session.add(new_game)
                    db.session.commit()
                    return redirect(url_for('main.joingame', game_id = 0, user_id = 0))
    else:
        return render_template('create_game.html', form = form)

@main.route('/joingame/<int:game_id>/<int:user_id>', methods=['GET','POST'])
@login_required
def joingame(game_id=0,user_id=0):
    form = StatForm()
    search = SearchForm()
    games = Game.query.all()
    if request.method == 'POST' and search.validate_on_submit():
        city = search.city.data.title()
        state = search.state.data.title()
        url = "https://geocoding-by-api-ninjas.p.rapidapi.com/v1/geocoding"
        querystring = {"city":city,"state":state,"country":"US"}
        headers={
            "X-RapidAPI-Key": "8e272dcadfmshca0c0e19694e049p12ab77jsn1c11e67b2682",
	        "X-RapidAPI-Host": "geocoding-by-api-ninjas.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers, params=querystring)
        if response.ok:
            location_data= response.json()
            for index in location_data:
                if index['state'] == state:
                    lat = index['latitude']
                    long = index['longitude']
                    url2 = "https://geocodeapi.p.rapidapi.com/GetNearestCities"
                    querystring2 = {"latitude":lat,"longitude":long,"range":"0"}
                    headers2 = {
                        "X-RapidAPI-Key": "8e272dcadfmshca0c0e19694e049p12ab77jsn1c11e67b2682",
                        "X-RapidAPI-Host": "geocodeapi.p.rapidapi.com"
                    }
                    response2 = requests.get(url2, headers=headers2, params=querystring2)
                    if response2.ok:
                        location_list = response2.json()
                        return render_template('join_game.html', games = games, form = form, search = search, location_list = location_list )
    
    elif request.method == 'POST' and form.validate_on_submit():
        print(user_id)
        print(game_id)
        game = Game.query.get(game_id)
        user = User.query.get(user_id)
        if int(form.points.data) >=10 and int(form.assists.data) >=10 and int(form.rebounds.data) >=10:
            user.triple_double = 'True'
        if int(form.points.data) ==0 and int(form.assists.data) ==0 and int(form.rebounds.data) ==0:
            user.snell = 'True'
        if int(form.points.data) >=50 or int(form.assists.data) >=30 or int(form.rebounds.data) >=30:
            user.sus = 'True'
        user.points = int(form.points.data) + user.points
        user.assists = int(form.assists.data) + user.assists
        user.rebounds = int(form.rebounds.data) + user.rebounds
        user.games_played = user.games_played + 1
        db.session.commit()
        game.participants.remove(user)
        db.session.commit()
        return render_template('join_game.html', games = games, form = form, game_id = game.id, search = search)
    
    else:
        return render_template('join_game.html', games = games, form = form, search = search )

@main.route('/closegame/<int:game_id>')
@login_required
def close_game(game_id):
    game = Game.query.get(game_id)
    if game.open == 'open':
        game.open = 'closed'
        db.session.commit()
        return redirect(url_for('main.joingame', user_id = 0, game_id = 0))
    else:
        game.open = 'open'
        db.session.commit()
        return redirect(url_for('main.joingame', user_id = 0, game_id = 0))

@main.route('/delete/<int:game_id>')
@login_required
def delete_game(game_id):
    game = Game.query.get(game_id)
    if current_user.id == game.user_id:
        db.session.delete(game)
        db.session.commit()
        return redirect(url_for('main.joingame', game_id=0, user_id = 0))
    
@main.route('/participate/<int:game_id>/<int:user>')
@login_required
def participate(game_id,user):
    user = User.query.filter_by(id = user).first()
    game = Game.query.get(game_id)
    check = 0
    if game:
        if game.amount == '3 vs 3':
            check = 6
        elif game.amount == '5 vs 5':
            check = 10
        if user in game.participants:
            game.participants.remove(user)
            db.session.commit()
            return redirect(url_for('main.joingame', game_id=0, user_id = 0))   
        else:
            if len(game.participants.all()) < check:
                game.participants.append(user)
                db.session.commit()
                return redirect(url_for('main.joingame', game_id=0, user_id = 0))
            else:
                return redirect(url_for('main.joingame', game_id=0, user_id = 0))
    else:
        return redirect(url_for('main.joingame', game_id=0, user_id = 0))
    
@main.route('/profile/<int:user_id>')
@login_required
def profile(user_id):
    user = User.query.get(user_id)
    return render_template('profile.html', user=user)
    
@main.route('/follow/<int:user_id>')
@login_required
def follow(user_id):
    user = User.query.get(user_id)
    if user:
        if user not in current_user.followed:
            current_user.followed.append(user)
            db.session.commit()
            return render_template('profile.html', user = user)
        else:
            current_user.followed.remove(user)
            db.session.commit()
            return render_template('profile.html', user = user)