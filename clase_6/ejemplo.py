import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2*np.pi, 100)
f = lambda x: np.sin(x)
print("Biseccion")
Biseccion(f, 3, 3.5, 1e-6)
print("")
print("Posicion Falsa")
PosicionFalsa(f, 3, 3.5, 1e-6)

plt.plot(x, np.sin(x))
plt.axhline(y=0, color='red', linestyle='--')
plt.xlabel('x')
plt.grid()
plt.show()