import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import Ceros as c

# Necesitamos encontnrar la profundidad h para un tanque con radio r = 2 y longitud L = 8 y con V = 12.5


# Parametros
r = 2
L = 8
V = 12.5
h = sp.symbols('x')


# Funcion
f = (r**2 * sp.acos((r - h) / h) - (r - h) * sp.sqrt(2 * r * h - h ** 2)) * L - V
f_lambda = sp.lambdify(h, f, 'numpy')

# Metodo abierto
sol_abierta, it_n = c.Newton(f, 1.3, 1e-6)
# Metodo cerrado
sol_cerrada = c.PosicionFalsa(f_lambda, 1.0, 1.2, 1e-6)

print(f"solucion abierta: {sol_abierta}")
print(f"solucion cerrada: {sol_cerrada}")


# Bosquejo de la grafica
h_range = np.linspace(1.1, 1.5, 100)
plt.figure(figsize=(8, 4))
plt.plot(h_range, f_lambda(h_range))
plt.axhline(0, color='red', linestyle='--')
plt.title("Bosquejo de la Funcion de Ceros - Ejercicio 1")
plt.xlabel("Profundidad h")
plt.ylabel("f(h)")
plt.grid(True)
plt.show()

# Justificacion: El valor h = 1.16 m es correcto ya que al ser un volumen de 12.5 m^3
# frente a una capacidad total de 100.5 m^3 la altura debe ser menor al radio del tanque.
