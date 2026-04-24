import numpy as np
import matplotlib.pyplot as plt

R = 3
V = 30

f_profu = lambda h: np.pi*h**2*((3*R-h)/3)-V
Biseccion(f_profu, 0, 6, 1e-6)


#Se realiza el grafico de la funcion de ceros para estimar un intervalo inical de busqueda
g = 32.17
x = 1.7

w = np.linspace(-5, -1e-3, 100)
omega = lambda w:-g/(2*w**2) * ((np.exp(w) - np.exp(-w))/2 - np.sin(w))-x
Biseccion(omega, -5, -1e-3, 1e-5)

plt.plot(w, omega(w))
plt.axhline(y=0, color='red', linestyle='--')
plt.xlabel('w')
plt.ylabel('f(w)')
plt.title('Plano inclinado')
plt.grid()
plt.show()

f_pro = lambda x: x**10-1

print("Posicion Falsa")
PosicionFalsa(f_pro, 0, 3, 1e-6)
print("")
print("Biseccion")
Biseccion(f_pro, 0, 3, 1e-6)