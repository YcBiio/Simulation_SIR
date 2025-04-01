import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.integrate import odeint
from matplotlib.widgets import Slider
import shared_config
import importlib
import os


# Fonction pour recharger `shared_config.py` dynamiquement
def reload_config():
    importlib.reload(shared_config)
    return shared_config.S0, shared_config.I0, shared_config.BETA, shared_config.LAMBDA


# Charger les valeurs actuelles
S0, I0, beta, lamda = reload_config()


# Modèle SIRD
def sird_model(y, t, beta):
    S, I, R, D = y
    dSdt = -beta * S * I / 1000000
    dIdt = beta * S * I / 1000000 - shared_config.GAMMA * I - shared_config.MU * I
    dRdt = shared_config.GAMMA * I
    dDdt = shared_config.MU * I
    return [dSdt, dIdt, dRdt, dDdt]


# Création du graphique
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.35)

# Initialisation des courbes avec une **grande précision temporelle**
t = np.linspace(0, lamda, 500)
y0 = [1000000 * S0, 1000000 * I0, 0, 0]
result = odeint(sird_model, y0, t, args=(beta,))
S, I, R, D = result.T

line_S, = ax.plot(t, S, label="Susceptibles", color='blue')
line_I, = ax.plot(t, I, label="Infectés", color='red')
line_R, = ax.plot(t, R, label="Rétablis", color='green')
line_D, = ax.plot(t, D, label="Décédés", color='black')

ax.set_xlabel("Temps (jours)")
ax.set_ylabel("Nombre d'individus")
ax.set_title("Évolution SIRD - Simulation Dynamique")
ax.legend()
ax.grid()

# Création des sliders
ax_S0 = plt.axes([0.15, 0.2, 0.3, 0.03])
ax_I0 = plt.axes([0.15, 0.15, 0.3, 0.03])
ax_beta = plt.axes([0.55, 0.2, 0.3, 0.03])
ax_lamda = plt.axes([0.55, 0.15, 0.3, 0.03])

s_S0 = Slider(ax_S0, 'S₀', 0, 1, valinit=S0, color='blue')
s_I0 = Slider(ax_I0, 'I₀', 0, 1, valinit=I0, color='red')
s_beta = Slider(ax_beta, 'β', 0, 1, valinit=beta, color='green')
s_lamda = Slider(ax_lamda, 'λ', 10, 200, valinit=lamda, color='black')


# Mettre à jour les sliders en continu
def update_slider(val=None):
    """ Met à jour les valeurs et synchronise avec Pygame. """
    global S0, I0, beta, lamda
    S0, I0, beta, lamda = s_S0.val, s_I0.val, s_beta.val, s_lamda.val

    # Mettre à jour `shared_config.py`
    with open("shared_config.py", "w") as f:
        f.write(f"S0 = {S0}\nI0 = {I0}\nBETA = {beta}\nLAMBDA = {lamda}\nUPDATED = True\n")

    # Envoyer un signal pour forcer la mise à jour de Pygame
    with open("update_signal.txt", "w") as signal:
        signal.write("UPDATE")


# Associer les sliders à la mise à jour dynamique
s_S0.on_changed(update_slider)
s_I0.on_changed(update_slider)
s_beta.on_changed(update_slider)
s_lamda.on_changed(update_slider)


# Animation ultra-fluide avec rafraîchissement rapide
def animate(frame):
    """ Met à jour les courbes de manière fluide et synchronisée. """
    reload_config()

    # Augmenter la résolution temporelle
    t_new = np.linspace(0, lamda, 500)
    y0 = [1000000 * S0, 1000000 * I0, 0, 0]
    result = odeint(sird_model, y0, t_new, args=(beta,))
    S, I, R, D = result.T

    line_S.set_data(t_new, S)
    line_I.set_data(t_new, I)
    line_R.set_data(t_new, R)
    line_D.set_data(t_new, D)

    ax.set_xlim(0, lamda)
    ax.set_ylim(0, 1000000)
    return line_S, line_I, line_R, line_D


ani = animation.FuncAnimation(fig, animate, interval=50, cache_frame_data=False)

plt.show()
