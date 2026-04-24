from pathlib import Path
import sys
# Agrega la raíz del proyecto al path de Python
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

'''
Hallar el ceros de P(x)  a partir de los siguientes datos; 


|x 	|0	| 0.5	| 1 	|1.5 	|2 	|2.5	 | 3	   |
|-------|-------|-------|-------|-------|-------|--------|---------|
|y	| 1.8421| 2.4694| 2.4921| 1.9047| 0.8509| −0.4112| −1.5727|



Utiliza la interpolacioón polinomial simple sobre:

- Usando 3 puntos de datos vecinos más cercanos
- Usando 4 puntos de datos vecinos más cercanos 
'''
import numpy as np
import matplotlib.pyplot as plt
import sel as s
import modelos as m
import Ceros as c

x_data = np.array([0, 0.5, 1, 1.5, 2, 2.5, 3])
y_data = np.array([1.8421, 2.4694, 2.4921, 1.9047, 0.8509, -0.4112, -1.5727])


