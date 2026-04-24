import numpy as np
import sympy as sp

g = sp.exp(2*x)*sp.sin(x)
P = Taylor(g, np.pi, 3)
x_values = [1, 4.5]
evaluacion(x_values, sp.lambdify(x, g), sp.lambdify(x, P))