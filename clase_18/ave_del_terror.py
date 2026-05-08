from pathlib import Path
import sys
# Agrega la raíz del proyecto al path de Python
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))



import numpy as np
import matplotlib.pyplot as plt
import modelos as m

x_data = np.array([0.7943,0.7079,1.0000,1.1220,1.6982,1.2023,1.9953,2.2387,2.5119,2.5119,3.1623,3.5481,4.4668,5.8884,6.7608,15.1360,15.8500])
y_data = np.array([0.0832,0.0912,0.1413,0.1479,0.2455,0.2818,0.7943,2.5119,1.4125,0.8913,1.9953,4.2658,6.3096,11.2202,19.9500,141.2500, 158.4893])

# m.escalas(x_data, y_data)

# modelo 1 : Escala x - sqrt(y)

R_modelo1 = m.coeficiente_determinacion(x_data, np.sqrt(y_data))

print(f'El coeficiente de determinacion del modelo 1 es: {R_modelo1}')

# Minimos cuadrados para le modelo 1

m, b = m.minimos_cuadrados(x_data, np.sqrt(y_data))
modelo1 = lambda x: m*x + b
x_values = np.linspace(min(x_data), max(x_data), 100)

plt.figure(figsize=(8, 4), dpi=80)
plt.subplot(121)
plt.scatter(x_data, np.sqrt(y_data), color='blue', label='minimos cuadrados')
plt.plot(x_values, modelo1(x_values), color='red', label='modelo 1')
plt.xlabel('x')
plt.ylabel(r'$\sqrt{y}$')
plt.legend()
plt.grid()

plt.subplot(122)
plt.scatter(x_data, y_data, color='blue')
modelo_no_lineal = lambda x: (m*x + b) ** 2
plt.plot(x_values, modelo_no_lineal(x_values), color='red')
plt.xlabel('Circunferencia del femur')
plt.ylabel('Peso del ave del terror')
plt.legend()
plt.grid()


# Modelo 2 : x**3 y
R_modelo2 = m.coeficiente_determinacion(x_data**3, y_data)
print(f'El coeficiente de determinacion del modelo 2 es: {R_modelo2}')

# Minimos cuadrados para le modelo 2
m2, b2 = m.minimos_cuadrados(x_data**3, y_data)

modelo2 = lambda x: m2*x + b2
x_values = np.linspace(min(x_data**3), max(x_data**3), 100)

plt.figure(figsize=(8, 4), dpi=80)
plt.subplot(121)
plt.scatter(x_data**3, y_data, color='blue', label='minimos cuadrados')
plt.plot(x_values, modelo2(x_values), color='red', label='modelo 2')
plt.xlabel(r'$x^3$')
plt.ylabel('y')
plt.legend()
plt.grid()

modelo_no_lineal2 = lambda x: (m2*x**3 + b2)
x_values2 = np.linspace(min(x_data), max(x_data), 100)
plt.figure(figsize=(8, 4), dpi=80)
plt.subplot(122)
plt.scatter(x_data, y_data, color='blue')
plt.plot(x_values2, modelo_no_lineal2(x_values2), color='red')
plt.xlabel('Circunferencia del femur')
plt.ylabel('Peso del ave del terror')
plt.legend()
plt.grid()
plt.show()