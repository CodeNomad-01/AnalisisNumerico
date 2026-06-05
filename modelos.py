import numpy as np
import sel as s
import sympy as sp
import matplotlib.pyplot as plt

def matriz(x_data):
    x = np.asarray(x_data, dtype=float)
    n = len(x)
    A = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            A[i, j] = x[i] ** j
    return A

def polinomial_simple(x_data, y_data):
    x = sp.symbols('x')
    A = matriz(x_data)
    coef = s.eliminacion_DD_pivoteo(A, y_data)
    polinomio = sum(coef[i] * x**i for i in range(len(x_data)))
    return sp.expand(polinomio)


def lagrange(x_data, y_data):
    x = sp.symbols('x')
    sumPolinomio = 0
    for i in range(len(x_data)):
        Li = 1
        for j in range(len(x_data)):
            if j != i:
                Li *= (x - x_data[j]) / (x_data[i] - x_data[j])
        sumPolinomio += Li * y_data[i]
    return sp.expand(sumPolinomio)


def minimos_cuadrados(x_data, y_data):
    n = len(x_data)
    Sx = sum(x_data)
    Sy = sum(y_data)
    Sxy = sum(x_data * y_data)
    Sx2 = sum(x_data ** 2)
    m = (n * Sxy - Sx * Sy) / (n * Sx2 - Sx ** 2)
    b = (Sy - m * Sx) / n
    return m, b

def escalas(xd, yd):
    plt.figure(figsize=(12, 12), dpi=50)

    plt.subplot(331)
    plt.plot(xd, yd, 'or', label='Datos observados')
    plt.title('datos originales', fontsize=10, fontweight='bold')
    plt.grid()
    plt.legend()
    plt.xlabel('x')
    plt.ylabel('y')
    # ---------------------------------
    plt.subplot(332)
    plt.plot(xd, yd**2, 'og', label=r'$y^2$')
    plt.title('transformacion y^2', fontsize=10, fontweight='bold')
    plt.grid()
    plt.legend()
    plt.xlabel('x')
    plt.ylabel(r'$y^2$')
    # ---------------------------------
    plt.subplot(333)
    plt.plot(xd, 1/yd, 'om', label=r'$1/y$')
    plt.title('transformacion 1/y', fontsize=10, fontweight='bold')
    plt.grid()
    plt.legend()
    plt.xlabel('x')
    plt.ylabel(r'$1/y$')
    # ---------------------------------
    plt.subplot(334)
    plt.plot(xd, np.sqrt(yd), 'oc', label=r'$\sqrt{y}$')
    plt.title('transformacion sqrt(y)', fontsize=10, fontweight='bold')
    plt.grid()
    plt.legend()
    plt.xlabel('x')
    plt.ylabel(r'$\sqrt{y}$')
    # ---------------------------------
    plt.subplot(335)
    plt.plot(xd, np.log(yd), 'ob', label=r'$\log(y)$')
    plt.title('transformacion log(y)', fontsize=10, fontweight='bold')
    plt.grid()
    plt.legend()
    plt.xlabel('x')
    plt.ylabel(r'$\log(y)$')
    # ---------------------------------
    plt.subplot(336)
    plt.plot(xd**2, yd, 'ob', label=r'$x^2$')
    plt.title('transformacion x^2', fontsize=10, fontweight='bold')
    plt.grid()
    plt.legend()
    plt.xlabel(r'$x^2$')
    plt.ylabel('y')
    # ---------------------------------
    plt.subplot(337)
    plt.plot(xd**3, yd, 'ob', label=r'$x^3$')
    plt.title('transformacion x^3', fontsize=10, fontweight='bold')
    plt.grid()
    plt.legend()
    plt.xlabel(r'$x^3$')
    plt.ylabel('y')
    # ---------------------------------
    plt.subplot(338)
    plt.plot(np.log(xd), yd, 'ob', label=r'$\log(x)$')
    plt.title('transformacion log(x)', fontsize=10, fontweight='bold')
    plt.grid()
    plt.legend()
    plt.xlabel(r'$\log(x)$')
    plt.ylabel('y')
    # ---------------------------------
    plt.subplot(339)
    plt.plot(np.log(xd), np.log(yd), 'ob', label=r'$\log(x),\log(y)$')
    plt.title('transformacion log(x),log(y)', fontsize=10, fontweight='bold')
    plt.grid()
    plt.legend()
    plt.xlabel(r'$\log(x)$')
    plt.ylabel(r'$\log(y)$')
    plt.show()

def coeficiente_determinacion(x, y):
    n = len(y)
    y_bar = sum(y) / n
    m, b = minimos_cuadrados(x, y)
    y_mod = lambda x: m*x + b
    numerador = sum((y - y_mod(x)) ** 2)
    denominador = sum((y - y_bar) ** 2)
    R2 = 1 - numerador / denominador
    return R2