import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import Ceros as c

# Se necesita hallar la fraccion vacia epsilon para un lecho con parametros especificos

def  f_ergun(e):
    return (10 * e ** 3 / (1 - e)) - (150 * (1 - e) / 1000) - 1.75

# fraccionn vaica usando el metodo de biseccion
sol_bis = c.Biseccion(f_ergun, 0.3, 0.7, 1e-6)

# fraccion vacia usando el metodo de Secante
sol_sec, iter_sec = c.Secante(f_ergun, 0.4, 0.5, 1e-6)

print(f"Epsilon (Biseccion): {sol_bis}")
print(f"Epsilon (Secante): {sol_sec}")

# Bosquejo de la grafica
e_vals = np.linspace(0.1, 0.9, 100)
plt.plot(e_vals, f_ergun(e_vals))
plt.axhline(0, color='black')
plt.title("Bosquejo Ergun")
plt.show()\

# Justificacion: El valor obtenido 0.46 es aceptable para la fraccion vacia 
# cumpliendo con la precision requerida por los metodos numericos aplicados