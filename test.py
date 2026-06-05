import Ceros as c
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import sel as sl
import modelos as ml
import ecuaciones as ec

# =============================================================================
# TIPO 1 — BISECCION (encontrar raices)
# Cuando: te dan una funcion f(x) y un intervalo [a, b].
# El metodo parte el intervalo a la mitad hasta que la raiz queda
# atrapada con la precision pedida. Necesita que f(a)*f(b) < 0.
# =============================================================================

# f(x) = (x+3)(x+1)x^2(x-1)^3(x-2)(x-4),  intervalo [-1.5, 2.5]
f = lambda x: (x+3)*(x+1)*x**2*(x-1)**3*(x-2)*(x-4)

print("=== TIPO 1: BISECCION ===")
print(f"f(-1.5) = {f(-1.5)}")   # positivo
print(f"f( 2.5) = {f(2.5)}")    # negativo -> hay raiz en el intervalo
raiz = c.Biseccion(f, -1.5, -0.5, 1e-6)   # intervalo estrecho -> converge a -1
print(f"Raiz aprox = {raiz:.6f}")
print()


# =============================================================================
# TIPO 2 — SISTEMAS DE ECUACIONES (Jacobi / Gauss-Seidel)
# Cuando: te dan Ax = b y piden radio espectral, iteraciones, o convergencia.
# Regla: radio espectral < 1 -> converge. Si no, usar solucion exacta.
# =============================================================================

A = np.array([[-2, 1, 12],
              [ 1,-2,-12],
              [ 0, 1,  2]], float)
b = np.array([4, 4, 0], float)
x0 = np.array([1.0, 1.0, 1.0])

print("=== TIPO 2: SISTEMAS DE ECUACIONES ===")

# -- Radio espectral de Jacobi: T = -D^(-1)(L+U) --
D   = np.diag(np.diag(A))
T_J = -np.linalg.inv(D) @ (A - D)
radio_J = max(abs(np.linalg.eigvals(T_J)))
print(f"Radio espectral Jacobi       = {radio_J:.4f}  -> converge: {radio_J < 1}")

# -- Radio espectral de Gauss-Seidel: T = (D-L)^(-1) U --
L   = -(np.tril(A) - D)
U   = -(np.triu(A) - D)
T_G = np.linalg.inv(D - L) @ U
radio_G = max(abs(np.linalg.eigvals(T_G)))
print(f"Radio espectral Gauss-Seidel = {radio_G:.4f}  -> converge: {radio_G < 1}")

# -- Iteraciones de Jacobi (aunque no converja, hace las n iteraciones) --
x_jac, its_jac = sl.jacobi_sumas(A, b, x0, tol=1e-4)
print(f"Jacobi  tras {its_jac} iter: x = {x_jac}")

# -- Solucion exacta (siempre disponible para verificar) --
x_exacta = np.linalg.solve(A, b)
print(f"Solucion exacta:              x = {x_exacta}")

# -- Verificar si un vector especifico es solucion: residual = Ax - b --
x_test   = np.array([-12.0, 4.0, -2.0])
residual = A @ x_test - b
print(f"Residual para x=[-12,4,-2]:  {residual}  -> es solucion: {np.allclose(residual, 0)}")
print()


# =============================================================================
# TIPO 3 — EDOs CON EULER
# Cuando: te dan y' = f(t,y) con condicion inicial y(t0) = y0.
# Si la EDO es de orden n, convertirla a sistema de n ecuaciones de orden 1.
# Indice para t objetivo: idx = int((t_obj - t0) / h)
# =============================================================================

# EDO de tercer orden:
#   t^3*y''' - t^2*y'' + 3t*y' - 4y = 5t^3*ln(t) + 9t^2
#   despejando y''':  y''' = [t^2*y'' - 3t*y' + 4y + 5t^3*ln(t) + 9t^2] / t^3
#
# Sistema de primer orden:
#   y1 = y    -> y1' = y2
#   y2 = y'   -> y2' = y3
#   y3 = y''  -> y3' = expresion de arriba
#
# CI: y(1)=0, y'(1)=1, y''(1)=3,  h=0.01,  t in [1,2]

def edo(t, y):
    y1, y2, y3 = y[0], y[1], y[2]
    dy1 = y2
    dy2 = y3
    dy3 = (t**2*y3 - 3*t*y2 + 4*y1 + 5*t**3*np.log(t) + 9*t**2) / t**3
    return np.array([dy1, dy2, dy3])

y0 = np.array([0.0, 1.0, 3.0])
t_vals, sol = ec.Euler(edo, 1, 2, 0.01, y0)
sol = np.array(sol)

y_vals  = sol[:, 0]
dy_vals = sol[:, 1]
d2y     = sol[:, 2]

idx = int((1.5 - 1) / 0.01)   # indice para t = 1.5

print("=== TIPO 3: EDO CON EULER ===")
print(f"y(1.5)   = {y_vals[idx]:.6f}   (esperado 1.048379)")
print(f"y'(1.5)  = {dy_vals[idx]:.6f}  (esperado 3.636917)")
print(f"y''(1.5) = {d2y[idx]:.6f}  (esperado 7.682628)")
print()


# =============================================================================
# TIPO 4 — POLINOMIOS A PARTIR DE PUNTOS O FUNCIONES
# Cuando: te dan n pares (x, y) o una funcion muestreada y piden el polinomio
# interpolante. Lagrange y Polinomial_simple deben dar el mismo resultado.
# Evaluar con sp.lambdify para obtener valores numericos.
# =============================================================================

x_data = np.array([1.0, 2.0, 3.0, 4.0])
y_data = np.array([1.0, 4.0, 9.0, 16.0])   # estos datos son y = x^2

x_sym = sp.symbols('x')

# Lagrange
P_lag = ml.lagrange(x_data, y_data)
f_lag = sp.lambdify(x_sym, P_lag)

# Polinomial simple (eliminacion gaussiana)
P_pol = ml.polinomial_simple(x_data, y_data)
f_pol = sp.lambdify(x_sym, P_pol)

print("=== TIPO 4: POLINOMIOS ===")
print(f"Lagrange:          P(x) = {P_lag}")
print(f"Polinomial simple: P(x) = {P_pol}")
print(f"Lagrange  en x=2.5 -> {f_lag(2.5):.4f}")
print(f"Pol.simple en x=2.5 -> {f_pol(2.5):.4f}")
print()


# =============================================================================
# TIPO 5 — AJUSTE DE MODELOS (R^2 y transformaciones)
# Cuando: te dan datos (x, y) y piden el modelo que mejor los representa.
# Flujo: escalas -> comparar R^2 -> ajustar con minimos_cuadrados -> recuperar
# parametros -> definir el modelo como lambda -> predecir nuevos valores.
# =============================================================================

# Datos: decaimiento de material radioactivo
t_d = np.array([0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5], float)
r_d = np.array([1, 0.994, 0.990, 0.985, 0.979, 0.977, 0.972, 0.969,
                0.967, 0.960, 0.956, 0.952], float)

print("=== TIPO 5: AJUSTE DE MODELOS ===")

# -- PASO 1: comparar R^2 de distintas transformaciones --
R2_lineal = ml.coeficiente_determinacion(t_d, r_d)
R2_log    = ml.coeficiente_determinacion(t_d, np.log(r_d))
R2_sqrt   = ml.coeficiente_determinacion(t_d, np.sqrt(r_d))
print(f"R^2  lineal  (t, r)        = {R2_lineal:.6f}")
print(f"R^2  log     (t, ln(r))    = {R2_log:.6f}")
print(f"R^2  sqrt    (t, sqrt(r))  = {R2_sqrt:.6f}")
print("-> El mayor R^2 indica la mejor transformacion")
print()

# -- PASO 2: ajustar el modelo exponencial r = A * exp(m*t) --
# lineariza como: ln(r) = m*t + ln(A)  ->  pendiente=m, intercepto=ln(A)
m, log_A = ml.minimos_cuadrados(t_d, np.log(r_d))
A = np.exp(log_A)
modelo_exp = lambda t: A * np.exp(m * t)
print(f"Modelo exponencial: r(t) = {A:.6f} * exp({m:.6f} * t)")

# -- PASO 3: ajustar el modelo raiz r = (m*t + b)^2 --
# lineariza como: sqrt(r) = m*t + b
m2, b2 = ml.minimos_cuadrados(t_d, np.sqrt(r_d))
modelo_sqrt = lambda t: (m2*t + b2)**2
print(f"Modelo raiz:        r(t) = ({m2:.6f}*t + {b2:.6f})^2")
print()

# -- PASO 4: predecir para valores nuevos --
print(f"Prediccion exponencial t=7  -> {modelo_exp(7):.6f}")
print(f"Prediccion exponencial t=10 -> {modelo_exp(10):.6f}")
print(f"Prediccion raiz        t=7  -> {modelo_sqrt(7):.6f}")
print(f"Prediccion raiz        t=10 -> {modelo_sqrt(10):.6f}")
print()

# -- GRAFICA comparativa (descomentar si se quiere ver) --
# t_plot = np.linspace(0, 6, 200)
# plt.figure(figsize=(8, 4))
# plt.plot(t_d, r_d, 'ko', label='Datos')
# plt.plot(t_plot, modelo_exp(t_plot),  'b-', label='Exponencial')
# plt.plot(t_plot, modelo_sqrt(t_plot), 'r-', label='Raiz cuadrada')
# plt.legend(); plt.grid(); plt.title("Ajuste de modelos"); plt.show()
