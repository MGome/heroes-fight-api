import random
import requests
from hero import Hero

class DataProcessing:
    def __init__(self, number_of_heroes):
        self.number_of_heroes = number_of_heroes
        self.valid_ids = []
        self.heroes_list = []

    def get_valid_ids(self):
        response_http = requests.get(f'https://akabab.github.io/superhero-api/api/all.json')
        for elem in response_http.json():
            self.valid_ids.append(elem['id'])

    def get_heroes(self):
        for i in range(self.number_of_heroes):
            hero_id = random.choice(self.valid_ids)
            self.valid_ids.remove(hero_id)
            hero_response = requests.get(f'https://akabab.github.io/superhero-api/api/id/{hero_id}.json')
            hero_name = hero_response.json()['name']
            hero_alignment = hero_response.json()['biography']['alignment']
            hero_base_stats = hero_response.json()['powerstats']
            hero_instance = Hero(i, hero_name, hero_alignment, hero_base_stats)
            self.heroes_list.append(hero_instance)

    def setup_data(self):
        self.get_valid_ids()
        self.get_heroes()
