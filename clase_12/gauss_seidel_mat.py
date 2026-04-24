import numpy as np
A = np.array([[10, -3, 5], [2, -13,7], [4, -8, 15]], float)
b = np.array([12, 23, 14], float)
x0 = np.ones_like(b)
tol = 1e-6
Nmax = 100

def gauss_seidel_mat(A, b, x0, tol):

    D = np.diag(np.diag(A))
    U = D - np.triu(A)
    L = D - np.tril(A)
    Tg = np.dot(np.linalg.inv(D - L), U)
    Cg = np.dot(np.linalg.inv(D - L), b)
    
    print(Tg)
    print(Cg)
    
    eigvalues, eigvector = np.linalg.eig(Tg)
    radio_espectral = max(abs(eigvalues))

    print(f'El radio espectral de la matriz es {radio_espectral}')

    if radio_espectral > 1:
        print('El metodo de Gauss-Seidel no converge para ningun valor de x0')
    else:
        error = 1
        while error > tol:
            x_new = np.dot(Tg, x0) + Cg
            error = max(abs(x_new - x0))
            x0 = x_new.copy()
        return x_new

def gauss_seidel_sumas(A, b, x0, tol):
    error = 1
    n = len(b)
    while error > tol:
        x_new = np.zeros_like(b)
        for i in range(n):
            suma1 = 0
            for j in range(i):
                suma1 += A[i, j] * x_new[j]
            suma2 = 0
            for j in range(i+1, n):
                suma2 += A[i, j] * x0[j]
            x_new[i] = (b[i] - suma1 - suma2) / A[i, i]
        error = max(abs(x_new - x0))
        x0 = x_new
    print(x_new, error)
# print("Gauss-Seidel con matriz: ", gauss_seidel_mat(A, b, x0, tol))
print("Gauss-Seidel con sumas: ", gauss_seidel_sumas(A, b, x0, tol))
