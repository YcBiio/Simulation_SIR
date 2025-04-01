class Config:
    # Taille de la population et durée de simulation
    POPULATION = 1000
    DAYS = 160  # Nombre de jours simulés

    # Paramètres épidémiologiques
    BETA = 0.3   # Taux de transmission (contacts par jour)
    GAMMA = 0.1  # Taux de guérison (1/durée moyenne de la maladie)
    MU = 0.02    # Taux de mortalité

    # Taille de la fenêtre Pygame
    WIDTH = 800
    HEIGHT = 600
