import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import Ceros as c

# Necesitamos determinar la tennsionn horizontal Ta para que un cable w = 12
# y0 = 6  alcance y = 15 x = 50

# parametros
w = 12
y0 = 6
x_val = 50
y = 15

Ta_sym = sp.symbols('x')

# Funcion
f_sim = (Ta_sym / w) * (sp.cosh((w / Ta_sym) * x_val)) + y0 - (Ta_sym / w) - y
f_num = sp.lambdify(Ta_sym, f_sim, 'numpy')

# Metodo newton
sol_ta, it_cat = c.Secante(f_num, 1600, 1700, 1e-4)
print(f"La tension horizontal Ta calculada es: {sol_ta}")
print(f"Iteraciones realizadas: {it_cat}")


# Bosquejo de la grafica
Ta_range = np.linspace(1000, 2500, 100)
plt.figure(figsize=(8, 4))
plt.plot(Ta_range, f_num(Ta_range))
plt.axhline(0, color='green', linestyle='--')
plt.title("Bosquejo de la Función de Ceros - Ejercicio 3 (Catenaria)")
plt.xlabel("Tensión Horizontal Ta")
plt.ylabel("f(Ta)")
plt.grid(True)
plt.show()

# justificacion: el valor de Ta = 1684.3 N es el unico que satisface la geometria
# del cable para que bajo un peso de 12 N/m y partirendo de una altura de 6m alcance
# los 15 m de altura a una distanncia horizontal de 50m