from flask import Flask, render_template, session, redirect, url_for, flash
from pokemon_logic import Pokemon, Wizard, Fighter
import random
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

@app.route('/')
def index():
    return render_template('index.html', pokemons=Pokemon.pokemons)

@app.route('/go')
def go():
    trainer_name = session.get('trainer_name')
    if not trainer_name:
        trainer_name = f"Trainer_{random.randint(1000, 9999)}"
        session['trainer_name'] = trainer_name

    if trainer_name not in Pokemon.pokemons:
        chance = random.randint(1, 4)
        if chance == 1:
            pokemon = Wizard(trainer_name)
        elif chance == 2:
            pokemon = Fighter(trainer_name)
        else:
            pokemon = Pokemon(trainer_name)

        Pokemon.pokemons[trainer_name] = pokemon
        flash(f"Поздравляем! Вы создали покемона {pokemon.name}!")

    # Всегда передаём pokemons в шаблон
    pokemon = Pokemon.pokemons[trainer_name]
    return render_template(
        'pokemon.html',
        name=pokemon.name,
        img_url=pokemon.img,
        info=pokemon.info(),
        trainer_name=trainer_name,
        pokemons=Pokemon.pokemons  # Передаём словарь покемонов
    )

@app.route('/battle/<opponent>')
def battle(opponent):
    trainer_name = session.get('trainer_name')

    if not trainer_name or trainer_name not in Pokemon.pokemons:
        flash("Сначала создайте покемона командой /go")
        return redirect(url_for('go'))

    if opponent not in Pokemon.pokemons:
        flash(f"У игрока {opponent} нет покемона!")
        return redirect(url_for('my_pokemons'))

    my_pokemon = Pokemon.pokemons[trainer_name]
    enemy_pokemon = Pokemon.pokemons[opponent]

    result = my_pokemon.attack(enemy_pokemon)

    Pokemon.pokemons[trainer_name] = my_pokemon
    Pokemon.pokemons[opponent] = enemy_pokemon

    return render_template(
        'battle.html',
        my_pokemon=my_pokemon,
        enemy_pokemon=enemy_pokemon,
        result=result,
        opponent=opponent,
        pokemons=Pokemon.pokemons  # Передаём словарь покемонов
    )

@app.route('/my_pokemons')
def my_pokemons():
    all_pokemons = [(name, pokemon.name, pokemon.hp, pokemon.power)
                   for name, pokemon in Pokemon.pokemons.items()]
    return render_template('my_pokemons.html', pokemons=all_pokemons, all_pokemons_dict=Pokemon.pokemons)

@app.route('/restore')
def restore():
    trainer_name = session.get('trainer_name')
    if trainer_name and trainer_name in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[trainer_name]
        pokemon.hp = random.randint(50, 150)
        pokemon.power = random.randint(10, 30)
        flash(f"Покемон {pokemon.name} восстановил силы! Здоровье: {pokemon.hp}, Сила: {pokemon.power}")
        return redirect(url_for('pokemon'))
    else:
        flash("Сначала создайте покемона!")
        return redirect(url_for('go'))

@app.route('/pokemon')
def pokemon():
    trainer_name = session.get('trainer_name')
    if trainer_name and trainer_name in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[trainer_name]
        return render_template(
            'pokemon.html',
            name=pokemon.name,
            img_url=pokemon.img,
            info=pokemon.info(),
            trainer_name=trainer_name,
            pokemons=Pokemon.pokemons
        )
    else:
        flash("У вас нет покемона! Создайте его командой /go")
        return redirect(url_for('go'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)