import numpy as np

def eliminacion_gaussiana(A, b):
  n = len(b)
  M = A.astype(float).copy()
  v = b.astype(float).copy()

  for i in range(n):
    for j in range(i + 1, n):
        factor = M[j][i] / M[i][i]
        M[j] = M[j] - factor * M[i]
        v[j] = v[j] - factor * v[i]

  x = np.zeros(n)
  for i in range(n - 1, -1, -1):
    suma = 0
    for j in range(i + 1, n):
        suma += M[i, j] * x[j]
    x[i] = (v[i] - suma) / M[i, i]

  return x



def eliminacion_DD_pivoteo(A, b):
    n = len(b)
    M = np.hstack((A, b.reshape(-1, 1))).astype(float)

    for i in range(n):

        max_row = np.argmax(abs(M[i:n, i])) + i
        if i != max_row:
            M[[i, max_row]] = M[[max_row, i]]

        for j in range(i + 1, n):
            if M[i, i] == 0:
                continue

            factor = M[j, i] / M[i, i]
            M[j] = M[j] - factor * M[i]

    for i in range(n):
        for j in range(i):
            M[i, j] = 0.0

    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        suma = 0
        for j in range(i + 1, n):
            suma += M[i, j] * x[j]
        x[i] = (M[i, n] - suma) / M[i, i]

    return x

def jacobi_sumas(A, b, x0, tol):
    Nmax = 50
    error = 1
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


def jacobi_mat(A, b, x0, tol):
    Nmax = 50
    D = np.diag(np.diag(A))
    U = D - np.triu(A)
    L = D - np.tril(A)
    inv_D = np.linalg.inv(D)
    Tj = np.dot(inv_D, L + U)
    Cj = np.dot(inv_D, b)

    eigvalues, eigvector = np.linalg.eig(Tj)
    radio_espectral = max(abs(eigvalues))

    if radio_espectral > 1:
        return None
    else:
        error = 1
        contador = 0
        while error > tol and contador < Nmax:
            x_new = np.dot(Tj, x0) + Cj
            error = max(abs(x_new - x0))
            x0 = x_new.copy()
            contador += 1
        return x_new, contador


def gauss_seidel_mat(A, b, x0, tol):
    Nmax = 50
    D = np.diag(np.diag(A))
    U = D - np.triu(A)
    L = D - np.tril(A)
    Tg = np.dot(np.linalg.inv(D - L), U)
    Cg = np.dot(np.linalg.inv(D - L), b)

    eigvalues, eigvector = np.linalg.eig(Tg)
    radio_espectral = max(abs(eigvalues))

    if radio_espectral > 1:
        return None
    else:
        error = 1
        contador = 0
        while error > tol and contador < Nmax:
            x_new = np.dot(Tg, x0) + Cg
            error = max(abs(x_new - x0))
            x0 = x_new.copy()
            contador += 1
        return x_new, contador

def gauss_seidel_sumas(A, b, x0, tol):
    Nmax = 50
    error = 1
    contador = 0
    n = len(b)
    x_new = np.zeros_like(b)
    while error > tol and contador < Nmax:
        for i in range(n):
            suma1 = 0
            for j in range(i):
                suma1 += A[i, j] * x_new[j]
            suma2 = 0
            for j in range(i+1, n):
                suma2 += A[i, j] * x0[j]
            x_new[i] = (b[i] - suma1 - suma2) / A[i, i]
        error = max(abs(x_new - x0))
        x0 = x_new.copy()
        contador += 1
    return x_new, contador