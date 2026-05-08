from ast import Yield
from pathlib import Path
import sys
# Agrega la raíz del proyecto al path de Python
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
import numpy as np
import matplotlib.pyplot as plt
import modelos as m


xd = np.array([1940,1945,1950,1955,1960,1965,1970,1975,1980,1985,1990])
yd = np.array([15000, 150000,250000,275000,270000,280000,290000,650000,1200000,1500000,2750000])

m.escalas(xd, yd)



print(coeficiente_determinacion(xd, np.log(yd)))