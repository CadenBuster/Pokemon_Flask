from flask import request, render_template, redirect, url_for, flash
import requests
from . import main
from app import db
from flask_login import current_user, login_required
from app.models import User, Game
from app.blueprints.main.forms import GameForm

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/games', methods = ['GET','POST'])
@login_required
def game():
    form = GameForm()
    if request.method == 'POST' and form.validate_on_submit():
        game_data = {
            'indoor': form.indoor.data,
            'score': form.score.data,
            'amount': form.amount.data,
            'user_id': current_user.id
        }

        new_game = Game()

        new_game.from_dict(game_data)

        db.session.add(new_game)
        db.session.commit()
        flash('You have created a game!')
        return redirect(url_for('main.joingame'))
    else:
        return render_template('create_game.html', form = form)

@main.route('/joingame')
@login_required
def joingame():
    games = Game.query.all()
    return render_template('join_game.html', games = games )

@main.route('/delete/<int:game_id>')
@login_required
def delete_game(game_id):
    game = Game.query.get(game_id)
    if current_user.id == game.user_id:
        db.session.delete(game)
        db.session.commit()
        return redirect(url_for('main.joingame'))
    
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
        if len(game.participants.all()) < check:
            if user not in game.participants:
                game.participants.append(user)
                db.session.commit()
                flash('You have joined this game!')
                return redirect(url_for('main.joingame'))
            else:
                game.participants.remove(user)
                db.session.commit()
                flash('You have left this game!')
                return redirect(url_for('main.joingame'))  
        else:
            flash(f'There are already {check} players signed up for this game!')
            return redirect(url_for('main.joingame'))
    else:
        flash('There has been an error!')
        return redirect(url_for('main.joingame'))

    