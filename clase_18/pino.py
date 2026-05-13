from pathlib import Path
import sys
# Agrega la raíz del proyecto al path de Python
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

#En los siguientes datos, X representa el diámetro de un pino, e Y es una medida de volumen-número de pies tablares dividido por 10. 


# |x   |   17 |   19 |   20 |   22 |   23 |   25 |   31 |   32 |   33 |   36  |   37   |   38   |   39|    41|
# |----|------|------|------|------|------|------|------|------|------|-------|--------|--------|-----|------|
# |y   | 19   | 25   | 32   | 51   | 57   | 71   | 141  | 123  | 187  | 192   | 205    | 252    | 248 | 294  |

import numpy as np
import matplotlib.pyplot as plt
import modelos as ml

x_data = np.array([17, 19, 20, 22, 23, 25, 31, 32, 33, 36, 37, 38, 39, 41])
y_data = np.array([19, 25, 32, 51, 57, 71, 141, 123, 187, 192, 205, 252, 248, 294])

