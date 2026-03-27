
import requests
import random

class Pokemon:
    pokemons = {}  # Хранилище всех покемонов

    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.img = self.get_img()
        self.name = self.get_name()
        self.hp = random.randint(50, 150)
        self.power = random.randint(10, 30)

    def get_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data['sprites']['front_default']
        else:
            return 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png'

    def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data['forms'][0]['name']
        else:
            return "Pikachu"

    def info(self):
        return (f"Имя: {self.name}\n"
                f"Здоровье: {self.hp}\n"
                f"Сила атаки: {self.power}")

    def attack(self, enemy):
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return (f"{self.pokemon_trainer} атакует {enemy.pokemon_trainer}!\n"
                    f"Урон: {self.power}. У {enemy.pokemon_trainer} осталось {enemy.hp} HP")
        else:
            enemy.hp = 0
            return f"Победа! {self.pokemon_trainer} победил {enemy.pokemon_trainer}!"

class Wizard(Pokemon):
    def attack(self, enemy):
        chance = random.randint(1, 5)
        if chance == 1:
            return f"{enemy.pokemon_trainer} уклонился от атаки!"
        return super().attack(enemy)

class Fighter(Pokemon):
    def attack(self, enemy):
        super_boost = random.randint(5, 15)
        original_power = self.power
        self.power += super_boost
        result = super().attack(enemy)
        self.power = original_power
        return result + f"\nСупер-удар: +{super_boost} силы!"



