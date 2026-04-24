import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import Ceros as c

# Parametros
gamma = 77 * 10**3
L = 1000
s = 1100

# a) s/L = sinh(beta)/beta  =>  beta = sinh(beta)/beta - s/L  = 0  (Newton, metodo abierto)

x = sp.symbols("x")
f_beta = sp.sinh(x) / x - (s / L)

beta_sol, it_n = c.Newton(f_beta, 1, 1e-6)
print(f"beta = {beta_sol:.6f}, iteraciones: {it_n}")

# b) Bosquejo de la funcion de ceros

f_beta_lamb = sp.lambdify(x, f_beta, "numpy")
beta_range = np.linspace(0.1, 3.0, 200)

plt.figure(figsize=(8, 4))
plt.plot(beta_range, f_beta_lamb(beta_range))
plt.axhline(0, color="red", linestyle="--")
plt.title("Bosquejo de la Funcion de Ceros")
plt.xlabel("beta")
plt.ylabel("f(beta)")
plt.grid(True)
plt.show()

# c) beta = gamma*L/(2*sigma_0) => sigma_0 = gamma*L/(2*beta)

sigma_0_sol = gamma * L / (2 * beta_sol)
sigma_max = sigma_0_sol * sp.cosh(beta_sol)
print(f"sigma_0 = {sigma_0_sol:.6f}, sigma_max = {float(sigma_max):.6f}")