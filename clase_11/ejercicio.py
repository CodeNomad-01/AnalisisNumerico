import numpy as np

A = np.array([[10, -3, 5], [-2, -13, 7], [4, -8, 15]], float)
b = np.array([12, 23, 14], float)
x0 = np.ones_like(b)

def jacobi_sumas(A, b, x0, tol):
    Nmax = 50
    error = 1
    tol = 1e-4
    contador = 0
    x_new = np.zeros_like(b)
    while error > tol and contador < Nmax:
        for i in range(len(b)):
            suma = 0
            for j in range(len(b)):
                if j != i:
                    suma += A[i, j] * x0[j]
            x_new[i] = (b[i] - suma) / A[i, i] 
        error = max(abs(x_new - x0))
        x0 = x_new.copy()
        contador += 1
    return x_new, contador

print(jacobi_sumas(A, b, x0, 1e-4))