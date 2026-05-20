from pathlib import Path
import sys
# Agrega la raíz del proyecto al path de Python
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np
import matplotlib.pyplot as plt
import ecuaciones as edo

# Supongamos que después de que Denise y Chad rompen su compromiso, Chad es reemplazadado por Craig 
# en los sentimientos de Denise, pero su relación sigue en gran medida el mismo patrón que tuvieron 
# Denise y Chad. Denise y Craig toman juntos una clase de Ingenería  donde se les asigna como compañeros
#  de laboratorio. Tienen que completar una nueva práctica cada $2\pi/c$ semanas, donde $c$ es una 
# constante positiva. Supongamos que el impacto del afecto de Denise por Craig a partir de la experiencia 
# de trabajar juntos agrega el término $\sin{ct}$ a la razón de cambio del cariño de ella al tiempo $t$.
#  Por ejemplo, durante la última parte de casa práctica de laboratorio, la tensión que sufre Denise al 
# intentar arreglárselas con la tardanza de Craig reduce su afecto hacia él. Sus emociones están descritas por:
 
# $$
#      x'=y+\sin{ct}; \quad y'=-4x
# $$
#  Estudie la solución para las emociones iniciales dadas por $x(0)=y(0)=0$, lo que significa que si ellos 
# no fueran forzados a trabajar juntos, no tendría sentimientos entre si. Como cambia esta relación a medida 
# que $c$ se aproxima a 2 y luego excede esto valor.
 
# Solucionar el sistema de ecuaciones diferenciales de primer orden por el método de Euler para $c=0.5, 
# \quad c=1.5, \quad c=2.2, \quad c=3$.

def trio(t, y):
    x = y[0]
    y = y[1]
    c = 2.2
    f1 = y + np.sin(c*t)
    f2 = -4*x
    return np.array([f1, f2])

t, romance = edo.Euler(trio, 0, 2*np.pi, 0.001, np.array([0, 0]))
denise = np.array(romance)[:,0]
craig = np.array(romance)[:,1]
print(denise)
print(craig)

plt.subplot(121)
plt.plot(t, denise, 'b')
plt.plot(t, craig, 'r')
plt.subplot(122)
plt.plot(denise, craig, 'g')
plt.show()