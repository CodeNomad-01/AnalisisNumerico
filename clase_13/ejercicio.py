import sys
from pathlib import Path

_PROYECTO = Path(__file__).resolve().parent.parent
if str(_PROYECTO) not in sys.path:
    sys.path.insert(0, str(_PROYECTO))

import numpy as np
import sel as sel

A = np.array([[10, -3, 5], [2, -13,7], [4, -8, 15]], float)
b = np.array([12, 23, 14], float)
x0 = np.ones_like(b)
tol = 1e-6
Nmax = 100

print(sel.gauss_seidel_sumas(A, b, x0, tol))