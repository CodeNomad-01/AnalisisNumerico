import sys
from pathlib import Path

_PROYECTO = Path(__file__).resolve().parent.parent
if str(_PROYECTO) not in sys.path:
    sys.path.insert(0, str(_PROYECTO))


import numpy as np
import sel as sel


# Consideremos una placa cuadrada de $30 \times 30$ unidades, en la cual se estudia la \textbf{distribución estacionaria de temperaturas}. Para ello, se utiliza el solución de ecuaciones lineales. En los bordes de la placa se imponen las siguientes condiciones de frontera:
# \[
# \begin{aligned}
# T(x,0) &= 30, \\
# T(x,30) &= 20, \\
# T(0,y) &= 25, \\
# T(30,y) &= 20.
# \end{aligned}
# \]
# La región se divide en una malla con 25 nodos interiores, donde cada incógnita $x_i$ representa la temperatura en el nodo correspondiente. El siguiente esquema muestra la  numeración de los nodos interiores:


# Cada nodo interior satisface la ecuación de diferencias finitas:

# $$
# x_{i,j} = \frac{1}{4}\big(x_{i+1,j} + x_{i-1,j} + x_{i,j+1} + x_{i,j-1}\big),
# $$
# lo cual conduce a un sistema de 25 ecuaciones lineales con 25 incógnitas. 
# La resolución de dicho sistema proporciona la distribución aproximada de temperaturas  en la placa.
