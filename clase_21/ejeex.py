from pathlib import Path
import sys
# Agrega la raíz del proyecto al path de Python
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Sea t^3y''' + t^2y'' + 3ty´+4y = 5t^3 lnt + 9t^2
# Condiciones iniciales: y(2) = 0, y'(2) = 1, y''(2) = 3
# intervalo t E [2, 3]
# convierta la ecuacion en un sistema de Ecuaciones de primer orden para 
# determinar los siguientes valores con un h: 0.01 con el metodo de Runge-Kutta de cuarto orden.

import numpy as np
import matplotlib.pyplot as plt
import ecuaciones as edo

def f(t, y):
    y1 = y[0]
    y2 = y[1]
    y3 = y[2]
    f1 = y2
    f2 = y3
    f3 = (5*np.log(t)+9/t+y3/t-(3*t**2)*y2+(4/t**3)*y1)
    return np.array([f1, f2, f3])

time, w = edo.Rk4(f, 2, 3, 0.01, np.array([0, 1, 3]))
print(time[40])
plt.plot(time, w)
plt.show()