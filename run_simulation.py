import multiprocessing
import subprocess
import sys

# Chemin correct du Python utilisé
python_exe = sys.executable

# Réinitialiser `shared_config.py` AVANT de lancer la simulation
def reset_shared_config():
    with open("shared_config.py", "w") as f:
        f.write("""# Paramètres initiaux réalistes pour une épidémie urbaine (~1 million d’habitants)
S0 = 0.47395833333333326  # 47.40% de la population initialement susceptible
I0 = 0.01      # 1% infectés au début
BETA = 0.3     # Taux de transmission
LAMBDA = 160   # Simulation sur 160 jours
GAMMA = 0.1    # Taux de guérison (1/durée moyenne de la maladie)
MU = 0.01      # Taux de mortalité (1% des infectés meurent)
UPDATED = False  # Indicateur de mise à jour
""")
    print("`shared_config.py` a été réinitialisé aux valeurs par défaut.")


def run_pygame():
    """ Exécute la simulation Pygame. """
    subprocess.run([python_exe, "main.py"], check=True)

def run_matplotlib():
    """ Exécute l'affichage des courbes SIRD. """
    subprocess.run([python_exe, "plot_sird.py"], check=True)

if __name__ == "__main__":
    multiprocessing.freeze_support()

    reset_shared_config()  # Réinitialise les valeurs avant de lancer les simulations

    p1 = multiprocessing.Process(target=run_pygame)
    p2 = multiprocessing.Process(target=run_matplotlib)

    p1.start()
    p2.start()

    p1.join()
    p2.join()
