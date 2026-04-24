from pathlib import Path
import sys
# Agrega la raíz del proyecto al path de Python
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Interpolacion: Polinomial Simple

#contruir un polinomio de maximo grado que contenga el siguiente conjunto de datos:

#|dia     |  0   |   6   |
#|Muestra | 6.67 | 17.33 |

# para aproxima el peso de una larva en el dia 4 de crecimiento

# El polinomio de grado 1 es:
# P(x) = a0 + a1*x
# y pasa por ccada uno de los datos, es decir:
# P(0) = 6.67 y P(6) = 17.33


import numpy as np
import sel as s
import matplotlib.pyplot as plt


x_data = np.array([[1, 0], [1, 6]])
y_data = np.array([6.67, 17.33])

s.eliminacion_gaussiana(x_data, y_data)

P = lambda x: 6.67 + 1.7766 * x

ux = np.linspace(min(x_data), max(x_data), 10)
plt.plot(x_data, y_data, 'or', label='Datos')
plt.plot(ux, P(ux), 'b', label='Polinomio')
plt.legend()
plt.show()