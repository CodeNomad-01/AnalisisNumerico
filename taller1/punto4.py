import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import Ceros as c

x = sp.symbols('x')

f_sim = x ** 4 + 20.75 * x ** 3 + 92.6 * x ** 2 + 73.69 * x
f_num = sp.lambdify(x, f_sim, 'numpy')

# Newton
raiz_newton, it_n = c.Newton(f_sim, -14, 1e-6)

# Biseccion
raiz_biseccion = c.Biseccion(f_num, -5, -4, 1e-6)

#Secante
raiz_secante, it_s = c.Secante(f_num, -1.5, -0.5, 1e-6)

# Posicion Falsa
raiz_falsa = c.PosicionFalsa(f_num, -0.5, 0.5, 1e-6)

print(f"Raiz Newton: {raiz_newton}")
print(f"Raiz Biseccion: {raiz_biseccion}")
print(f"Raiz Secante: {raiz_secante}")
print(f"Raiz Posicion Falsa: {raiz_falsa}")


s_graf = np.linspace(-16, 1, 400)
plt.figure(figsize=(10, 5))
plt.plot(s_graf, f_num(s_graf))
plt.axhline(0, color='red', linestyle='--')
plt.title("Bosquejo de Raíces del Denominador - Ejercicio 4")
plt.grid(True)
plt.show()

# Primero se descompuso en fracciones parciales la funcion, se determino las raices
# del polinomio del denominador D(s) raiz  s=0 por inspeccion ya uqe todos los terminos
# dependen de s. Al sustituir los valores en el polinomio orignal D(s), el resultado tiende a cero
# dentro de la tolerancia (10^-6)