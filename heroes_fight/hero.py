import random

class Hero:
    def __init__(self, hero_id, name, alignment, base_stats):
        self.id = hero_id
        self.name = name
        self.alignment = alignment
        self.base_stats = base_stats
        self.hp = 0
        self.partial_hp = 0
        self.fb = 0
        self.mental = 0
        self.strong = 0
        self.fast = 0
        self.selected_attack = {}

    def select_attack(self):
        '''
        Se selecciona aleatoriamente un ataque de un determinado héroe.
        Se guarda como un diccionario el nombre del ataque y su potencia,
        con fin de mostrar el nombre del ataque en el log de eventos.
        '''
        attack_list = [self.mental, self.strong, self.fast]
        selected_attack = random.choice(attack_list)
        attack_name = ['mental', 'strong', 'fast'][attack_list.index(selected_attack)]
        self.selected_attack = {'name': attack_name, 'power': selected_attack}
        