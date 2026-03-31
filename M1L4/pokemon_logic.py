
import requests
import random
from datetime import datetime, timedelta

class Pokemon:
    pokemons = {}  # Хранилище всех покемонов

    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 898)
        self.img = self.get_img()
        self.name = self.get_name()
        self.hp = random.randint(50, 150)
        self.power = random.randint(10, 30)
        # Гарантированно инициализируем атрибут
        self.last_feed_time = None
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
                f"Сила атаки: {self.power}"
                f"Последнее кормление: {self.last_feed_time.strftime('%H:%M:%S') if self.last_feed_time else 'Не кормился'}")

    def attack(self, enemy):
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return (f"{self.pokemon_trainer} атакует {enemy.pokemon_trainer}!\n"
                    f"Урон: {self.power}. У {enemy.pokemon_trainer} осталось {enemy.hp} HP")
        else:
            enemy.hp = 0
            return f"Победа! {self.pokemon_trainer} победил {enemy.pokemon_trainer}!"
    def feed(self, feed_interval = 20, hp_increase = 10 ):
        current_time = datetime.now()  
        if self.last_feed_time is None:
            self.hp += hp_increase
            self.last_feed_time = current_time
            return f"Здоровье покемона увеличено. Текущее здоровье: {self.hp}"

        delta_time = timedelta(hours=feed_interval)  
        if (current_time - self.last_feed_time) > delta_time:
            self.hp += hp_increase
            self.last_feed_time = current_time
            return f"Здоровье покемона увеличено. Текущее здоровье: {self.hp}"
        else:
            next_feed_time = self.last_feed_time + delta_time
            return f"Следующее время кормления покемона: {next_feed_time.strftime('%H:%M:%S')}"
class Wizard(Pokemon):
    def attack(self, enemy):
        chance = random.randint(1, 5)
        if chance == 1:
            return f"{enemy.pokemon_trainer} уклонился от атаки!"
        return super().attack(enemy)
    def feed(self, feed_interval = 20 , p_increase = 20):
        return super().feed(feed_interval, p_increase)
class Fighter(Pokemon):
    def attack(self, enemy):
        super_boost = random.randint(5, 15)
        original_power = self.power
        self.power += super_boost
        result = super().attack(enemy)
        self.power = original_power
        return result + f"\nСупер-удар: +{super_boost} силы!"
    def feed(self, feed_interval = 10 , p_increase = 10):
        return super().feed(feed_interval, p_increase)



