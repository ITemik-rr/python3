
import random
import requests

class Pokemon:
    pokemons = {}

    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)

        data = self._fetch_pokemon_data()

        if data:
            self.name = data['name']
            self.img = data['sprites']['front_default']
            self.height = data['height'] 
            self.weight = data['weight']  
            self.types = [t['type']['name'] for t in data['types']]
            self.abilities = [a['ability']['name'] for a in data['abilities']]
            self.stats = {
                stat['stat']['name']: stat['base_stat']
                for stat in data['stats']
            }
            self.moves = [m['move']['name'] for m in data['moves'][:4]] 
        else:

            self.name = "Pikachu"
            self.img = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png"
            self.height = 4
            self.weight = 60
            self.types = ["electric"]
            self.abilities = ["static"]
            self.stats = {"hp": 35, "attack": 55, "defense": 40, "special-attack": 50, "special-defense": 50, "speed": 90}
            self.moves = ["thunder-shock", "growl", "quick-attack", "thunderbolt"]

        Pokemon.pokemons[pokemon_trainer] = self

    def _fetch_pokemon_data(self):
        """Получает полные данные покемона через API"""
        url = f"https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Ошибка API: статус {response.status_code} для ID {self.pokemon_number}")
                return None
        except requests.RequestException as e:
            print(f"Ошибка сети: {e}")
            return None

    def info(self):
        """Возвращает подробную информацию о покемоне"""
        types_str = ", ".join(self.types).title()
        abilities_str = ", ".join(self.abilities).title()

        info_text = (
            f"🤴 Тренер: {self.pokemon_trainer}\n"
            f"🦊 Имя: {self.name.title()}\n"
            f"📏 Рост: {self.height / 10} м\n"  # переводим в метры
            f"⚖️ Вес: {self.weight / 10} кг\n"  # переводим в кг
            f"🔥 Тип: {types_str}\n"
            f"✨ Способности: {abilities_str}\n"
        )

        stats_text = "📊 Статы:\n"
        for stat_name, stat_value in self.stats.items():
            stats_text += f"  {stat_name.replace('-', ' ').title()}: {stat_value}\n"

        moves_text = f"💥 Атаки: {', '.join(self.moves).title()}"

        return info_text + stats_text + moves_text

    def show_img(self):
        return self.img

    def get_type(self):

        return self.types

    def get_stats(self):

        return self.stats

    def get_moves(self):

        return self.moves

    def change_name(self, new_name):

        self.name = new_name
        return f"Имя покемона изменено на {self.name}"

    def add_move(self, move_name):
       
        if len(self.moves) < 4 and move_name not in self.moves:
            self.moves.append(move_name)
            return f"Атака {move_name} добавлена!"
        else:
            return "Нельзя добавить больше 4 атак или атака уже есть"

    def level_up(self, stat_boost=5):

        for stat in self.stats:
            self.stats[stat] += stat_boost
        return f"{self.name} повысил уровень! Все статы увеличены на {stat_boost}"