import os
import random
import smtplib
import ssl
from email.message import EmailMessage
from dotenv import load_dotenv

class Simulation:
    def __init__(self, team_one, team_two):
        self.round = 0
        self.has_a_winner = False
        self.winner = 0
        self.team_one = team_one
        self.team_two = team_two
        self.removed_team_one = []
        self.removed_team_two = []
        self.mail_body = ''
        self.winner_text = ''
   
    def show_teams(self):
        '''
        Se itera sobre las listas de ambos equipos y se muestran los
        nombres en conjunto de la afiliación del equipo.
        '''
        print('Miembros del equipo 1')
        for member in self.team_one.members:
            print(member.name)
        print(f'Afiliación del equipo: {self.team_one.alignment}')
        print('\n')
        print('Miembros del equipo 2')
        for member in self.team_two.members:
            print(member.name)
        print(f'Afiliación del equipo: {self.team_two.alignment}')

    def setup_teams(self):
        '''
        Método que setea las condiciones para iniciar la partida,
        en primer lugar obtiene el alignment de cada equipo y
        actualiza las estadísticas para los miembros de ambos
        equipos.
        '''
        self.team_one.set_alignment()
        self.team_two.set_alignment()
        self.team_one.update_hero_stats()
        self.team_two.update_hero_stats()

    def get_alive_members(self):
        '''
        Método que busca mostrar los miembros restantes vivos
        de cada equipo.
        '''
        print('Miembros vivos del equipo 1:')
        for member in self.team_one.members:
            print(f'{member.name} (HP: {member.partial_hp})')
        print('\n')
        print('Miembros vivos del equipo 2:')
        for member in self.team_two.members:
            print(f'{member.name} (HP: {member.partial_hp})')
        print('\n')
  
    def init_fight(self):
        '''
        Método que inicia la pelea entre dos personajes de equipos
        contrarios. Ambos son elegidos aleatoriamente, donde el que
        ataca primero estará determinado por la estadística de
        velocidad real.
        Cuando un personaje muere es eliminado de la lista de su
        equipo.
        '''
        team_one_fighter = random.choice(self.team_one.members)
        team_two_fighter = random.choice(self.team_two.members)
        encounter_text = f'Enfrentamiento: {team_one_fighter.name} (Equipo 1) vs {team_two_fighter.name} (Equipo 2)'
        self.mail_body += encounter_text + '<br>'
        print(encounter_text)
        if team_one_fighter.base_stats['speed'] > team_two_fighter.base_stats['speed']:
            ## Ataca primero el luchador 1
            self.attack_simulation(team_one_fighter, team_two_fighter)
        elif team_two_fighter.base_stats['speed'] > team_one_fighter.base_stats['speed']:
            ## Ataca primero el luchador 2
            self.attack_simulation(team_two_fighter, team_one_fighter)
        else:
            ## Caso en que ambos tienen la misma velocidad, se define aleatoriamente
            fighters = [team_one_fighter, team_two_fighter]
            first_to_attack = random.choice(fighters)
            fighters.remove(first_to_attack)
            self.attack_simulation(first_to_attack, fighters[0])

    def attack_simulation(self, first, second):
        '''
        Método que simula una pelea, recibe dos instancias de héroes
        que siguen la siguiente regla:
        First: Primero en atacar, Second: Segundo en atacar
        Ambos se atacan hasta que uno de los dos tenga HP
        menor o igual a 0.
        '''
        battle_finished = False
        while not battle_finished:
            first.select_attack()
            first_attack_name = first.selected_attack['name']
            first_attack_power = first.selected_attack['power']
            print(f'{first.name} ha atacado a {second.name} con {first_attack_name} ({first_attack_power} de daño)')
            second.partial_hp -= first_attack_power
            if second.partial_hp <= 0:
                second.partial_hp = 0
                result_text = f'{second.name} ha muerto :(. El ganador es {first.name}'
                self.mail_body += result_text + '<br>'
                print(f'{second.name} ha muerto :(. El ganador es {first.name}')
                self.remove_hero_from_list(second)
                battle_finished = True
            else:
                print(f'{second.name} ha quedado con {second.partial_hp} de HP')
                second.select_attack()
                second_attack_name = second.selected_attack['name']
                second_attack_power = second.selected_attack['power']
                print(f'{second.name} ha atacado a {first.name} con {second_attack_name} ({second_attack_power} de daño)')
                first.partial_hp -= second_attack_power
                if first.partial_hp <= 0:
                    first.partial_hp = 0
                    result_text = f'{first.name} ha muerto :(. El ganador es {second.name}'
                    self.mail_body += result_text + '<br>'
                    print(result_text)
                    self.remove_hero_from_list(first)
                    battle_finished = True
                else:
                    print(f'{first.name} ha quedado con {first.partial_hp} de HP')

    def remove_hero_from_list(self, hero):
        '''
        Método que recibe una instancia de héroe,
        busca eliminar de la lista de su equipo
        a un personaje que perdió su pelea.
        '''
        if hero in self.team_one.members:
            self.team_one.members.remove(hero)
            self.removed_team_one.append(hero)
        else:
            self.team_two.members.remove(hero)
            self.removed_team_two.append(hero)

    def restart_hp(self):
        '''
        Método que itera sobre todas las listas de
        equipos. Busca restaurar el HP de cada personaje
        a su valor inicial para iniciar la siguiente
        ronda.
        '''
        for member in self.team_one.members:
            member.partial_hp = member.hp

        for member in self.team_two.members:
            member.partial_hp = member.hp

    def setup_next_round(self):
        '''
        Método que restaura los equipos iniciales incluyendo
        aquellos personajes que perdieron su pelea. Busca
        restaurar los equipos para iniciar la siguiente ronda.
        '''
        self.team_one.members.extend(self.removed_team_one)
        self.team_two.members.extend(self.removed_team_two)
        self.restart_hp()

    def start_round(self):
        '''
        Método de control de flujo general. Inicia una ronda y
        determina cuando un equipo ganó la ronda y/o partida.
        '''
        self.round += 1
        separator = 10 * '-'
        print(f'\n{separator} RONDA #{self.round} {separator}\n')
        self.mail_body += '<p><b>' + f'RONDA {self.round}:' + '</b></p>'
        while len(self.team_one.members) > 0 and len(self.team_two.members) > 0:
            self.get_alive_members()
            self.init_fight()
            print('\n')

        if len(self.team_one.members) > 0:
            round_winner_text = '¡Ha ganado el equipo 1!'
            print(round_winner_text)
            self.team_one.victories_count += 1
            if self.team_one.victories_count == 2:
                self.winner = 1
                self.has_a_winner = True
        else:
            round_winner_text = '¡Ha ganado el equipo 2!'
            print(round_winner_text)
            self.team_two.victories_count += 1
            if self.team_two.victories_count == 2:
                self.winner = 2
                self.has_a_winner = True
        self.mail_body += round_winner_text + '<br>'
        if not self.has_a_winner:
            ## En caso de que no haya un ganador se reincia el HP de los personajes
            self.setup_next_round()
    
    def check_if_send_results(self):
        '''
        Método que consulta al usuario si es que desea
        enviar los resultados por mail.
        '''
        should_send = int(input('¿Deseas enviar los resultados por email? (0: No, 1: Sí)\n'))
        if should_send > 0:
            receiver = input('Ingresa la dirección a la que deseas enviar los resultados: ')
            self.send_email(receiver)

    def send_email(self, receiver):
        '''
        Método que envía los resultados por mail. En primer
        lugar obtiene los valores almacenados en el .env,
        para luego dar formato al mail. El body que se envía
        en el mail es en formato HTML, para así dar el formato
        requerido.
        La estructura general de instanciar un mail y el uso
        básico de smtp fue obtenido de la siguiente fuente:
        https://realpython.com/python-send-email/
        '''
        load_dotenv()
        sender = os.environ.get('MAIL_SENDER')
        password = os.environ.get('MAIL_PASSWORD')
        subject = 'Resultados Pelea de Personajes'
        em_instance = EmailMessage()
        em_instance['From'] = sender
        em_instance['To'] = receiver
        em_instance['Subject'] = subject
        body = self.set_html_body()
        em_instance.set_content(body, subtype='html')
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            try:
                smtp.login(sender, password)
                smtp.sendmail(sender, receiver, em_instance.as_string())
                print('Correo enviado exitosamente')
            except Exception as ex:
                print(f'Lo siento, no se ha podido enviar el mail. Error: {ex}')

    def set_html_body(self):
        '''
        Método que genera el cuerpo del mail a enviar.
        '''
        html_text = f"""\
            <html>
                <head></head>
                <body> 
                    {self.mail_body}
                </body>
            </html>
            """
        return html_text
