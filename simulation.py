import pygame
import random
import time
from config import Config

def update_simulation(population):
    """ Met à jour l'état des individus : mouvement, infection et récupération. """
    for individual in population:
        individual.move()  # Ajout du mouvement

        # Gestion de l'infection
        if individual.state == "infected":
            for other in population:
                if other.state == "susceptible":
                    distance = ((individual.x - other.x) ** 2 + (individual.y - other.y) ** 2) ** 0.5
                    if distance < 10 and random.random() < 0.03:  # Taux d'infection ajustable
                        other.state = "infected"
                        other.infection_time = time.time()

            # Vérification de la guérison ou de la mort après un certain temps
            if individual.infection_time and time.time() - individual.infection_time > 5:
                individual.state = "recovered" if random.random() > Config.MU else "dead"

def draw_population(screen, population):
    """ Dessine chaque individu sur l'écran selon son état de santé. """
    for individual in population:
        color = (0, 0, 255) if individual.state == "susceptible" else \
                (255, 0, 0) if individual.state == "infected" else \
                (0, 255, 0) if individual.state == "recovered" else \
                (100, 100, 100)  # Gris pour les morts

        pygame.draw.circle(screen, color, (int(individual.x), int(individual.y)), 5)
