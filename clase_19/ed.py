from pathlib import Path
import sys
# Agrega la raíz del proyecto al path de Python
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
import ecuaciones as edo
import matplotlib.pyplot as plt


f = lambda t,y: 0.28782*y*t
t, w_res = edo.Euler(f, 0, 1, 0.25, 0)

plt.plot(t, w_res, 'o')
plt.show()