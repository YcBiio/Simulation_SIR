import random
from config import Config

class Individual:
    def __init__(self):
        self.x = random.uniform(0, Config.WIDTH)
        self.y = random.uniform(0, Config.HEIGHT)
        self.vx = random.uniform(-1, 1)  # Vitesse horizontale
        self.vy = random.uniform(-1, 1)  # Vitesse verticale
        self.state = "susceptible"  # État initial
        self.infection_time = None

    def move(self):
        """ Déplace l'individu en tenant compte des bords de l'écran """
        self.x += self.vx
        self.y += self.vy

        # Gérer les rebonds sur les bords de l'écran
        if self.x < 0 or self.x > Config.WIDTH:
            self.vx *= -1
        if self.y < 0 or self.y > Config.HEIGHT:
            self.vy *= -1
