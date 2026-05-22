from pathlib import Path
import sys
# Agrega la raíz del proyecto al path de Python
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


import numpy as np
import matplotlib.pyplot as plt
import ecuaciones as edo

def paracaidista(t, y):
    x = y[0]
    v = y[1]
    f1 = v
    f2 = -9.8 - (0.225/90)*v**2
    return np.array([f1, f2])


t, caida = edo.Euler(paracaidista, 0, 10, 0.0001,[1000, 0])
distancia = np.array(caida)[:, 0]
velocidad = np.array(caida)[:, 1]
print(t[40000], distancia[40000])


# calculo de tiempo de caida
for i in range(len(t)):
    if distancia[i] < 0:
        tiempo_caida = t[i]
        break
print(f"Tiempo de caida: {tiempo_caida}")

def f(t, y):
    return t * np.exp(3*t)-2*y

t, w = edo.Rk4(f, 0, 1, 0.0001, 1)
print(t, w)

plt.figure(figsize=(6, 4), dpi=100)
plt.plot(t, w)
plt.grid()
plt.show()


# plt.figure(figsize=(6, 4), dpi=100)
# plt.subplot(121)
# plt.plot(t, distancia)
# plt.xlim(8, 10)
# plt.grid()
# plt.subplot(122)
# plt.plot(velocidad, distancia)
# plt.tight_layout()

# plt.show()