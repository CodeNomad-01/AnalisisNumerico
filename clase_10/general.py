import numpy as np

A = np.array([
    [3,  2,  1],
    [ 6, -8, -2],
    [ 1, -1, -2]
])
b = np.array([2, 1, 3])

def eliminacion_DD(A,b):
  matriz_a = np.hstack((A, b.reshape(-1, 1))).astype(float)
  n=len(b)
  x_solucion = np.zeros_like(b)


  for j in range(n):
    for i in range(j+1, n):
      factor = matriz_a[i,j]/matriz_a[j,j]
      matriz_a[i, 0:n+1] = matriz_a[i, 0:n+1] - factor * matriz_a[j, 0:n+1]
  print(matriz_a)

  for k in range(n-1, -1, -1):
    x_solucion[k]= (matriz_a[k, n] - np.dot(matriz_a[k, k+1:n], x_solucion[k+1:n]))/matriz_a[k, k]

eliminacion_DD(A, b)


B = np.array([[-1, 2, 0], [2, -3, 1], [0, 1, 2]])
eigvalues, eigvector = np.linalg.eig(B)
radio_espectral = max(abs(eigvalues))
print(f'Los valores propios de la matriz son {}')