from data_processing import DataProcessing
from simulation import Simulation
from team  import Team

NUMBER_OF_HEROES = 10
simulation_data = DataProcessing(NUMBER_OF_HEROES)
simulation_data.setup_data()

team_one = Team(simulation_data.heroes_list[:5])
team_two = Team(simulation_data.heroes_list[5:])
simulation = Simulation(team_one, team_two)
simulation.setup_teams()
simulation.show_teams()
while not simulation.has_a_winner:
    simulation.start_round()

final_winner_text = f'\n¡El vencedor de la batalla es el equipo {simulation.winner}!'
print(final_winner_text)
simulation.winner_text += '<b>' + final_winner_text + '</b>'
simulation.check_if_send_results()
