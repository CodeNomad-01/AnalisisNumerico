from re import X
import numpy as np
import sel as s

def matriz(x_data):
    x = np.asarray(x_data, dtype=float)
    n = len(x)
    A = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            A[i, j] = x[i] ** j
    return A

def polinomial_simple(x_data, y_data):
    A = matriz(x_data)
    coef = s.eliminiacion_DD_pivoteo(A, y_data)
    polinomio = sum(coef[i] * (x_data ** i) for i in range(len(x_data)))
    return polinomio


def lagrange(x_data, y_data):
    sumPolinomio = 0
    for i in range(len(x_data)):
        Li = 1
        for j in range(len(x_data)):
            if j != i:
                Li *= (x - x_data[j]) / (x_data[i] - x_data[j])
        sumPolinomio += Li * y_data[i]
    return sumPolinomio