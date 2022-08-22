import random

class Team:
    def __init__(self, heroes_list):
        self.members = heroes_list
        self.alignment = ''
        self.victories_count = 0

    def set_alignment(self):
        good_counter = 0
        bad_counter = 0
        for member in self.members:
            if member.alignment == 'good':
                good_counter += 1
            else:
                bad_counter += 1
        self.alignment = 'good' if good_counter > bad_counter else 'bad'
    
    def update_hero_stats(self):
        for member in self.members:
            partial_fb = 1 + random.randint(0,9)
            member.fb = partial_fb if member.alignment == self.alignment else partial_fb**(-1)
            member.hp = self.calculate_member_hp(member.base_stats)
            member.partial_hp = member.hp
            for stat in member.base_stats.keys():
                actual_stamina = random.randint(0,9)
                base = member.base_stats[stat]
                calculated_stat = ((2*base + actual_stamina)/1.1)*member.fb
                member.base_stats[stat] = calculated_stat
            self.calculate_member_attacks(member)
            print('\n')

    def calculate_member_hp(self, stats):
        actual_stamina = random.randint(0,9)
        stats_relation = (stats['strength']*0.8 + stats['strength']*0.7 + stats['power'])/2
        partial_hp = stats_relation*(1 + (actual_stamina/10)) + 100
        return partial_hp
    
    def calculate_member_attacks(self, member):
        stats = member.base_stats
        fb = member.fb
        mental = (stats['intelligence']*0.7 + stats['speed']*0.2 + stats['combat']*0.1) * fb
        strong = (stats['strength']*0.6 + stats['power']*0.2 + stats['combat']*0.2) * fb
        fast = (stats['speed']*0.55 + stats['durability']*0.25 + stats['strength']*0.2) * fb
        member.mental = mental
        member.strong = strong
        member.fast = fast
