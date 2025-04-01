import pygame
import shared_config
import importlib
import os
from config import Config
from individual import Individual
from simulation import update_simulation, draw_population

def main():
    pygame.init()
    screen = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))
    clock = pygame.time.Clock()

    # Charger les valeurs initiales
    importlib.reload(shared_config)
    Config.POPULATION = 1000
    Config.BETA = shared_config.BETA
    Config.LAMBDA = shared_config.LAMBDA

    # Initialisation de la population
    population = []
    for i in range(Config.POPULATION):
        individual = Individual()
        if i < int(shared_config.I0 * Config.POPULATION):
            individual.state = "infected"
        else:
            individual.state = "susceptible"
        population.append(individual)

    running = True
    while running:
        screen.fill((0, 0, 0))

        # Vérifier si `update_signal.txt` existe
        if os.path.exists("update_signal.txt"):
            print("Mise à jour des valeurs en direct...")

            # Lire le fichier et le fermer immédiatement
            try:
                with open("update_signal.txt", "r") as f:
                    _ = f.read()  # Lire sans utiliser le contenu

                # Recharger `shared_config.py`
                importlib.reload(shared_config)
                Config.BETA = shared_config.BETA
                Config.LAMBDA = shared_config.LAMBDA

                # Réinitialiser la population avec les nouvelles valeurs
                population = []
                for i in range(Config.POPULATION):
                    individual = Individual()
                    if i < int(shared_config.I0 * Config.POPULATION):
                        individual.state = "infected"
                    else:
                        individual.state = "susceptible"
                    population.append(individual)

                # Supprimer `update_signal.txt` en toute sécurité
                os.remove("update_signal.txt")
            except PermissionError:
                print("Impossible de supprimer `update_signal.txt`, il est encore utilisé.")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        update_simulation(population)
        draw_population(screen, population)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
