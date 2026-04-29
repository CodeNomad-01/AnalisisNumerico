import numpy as np
import sel as sel

A = np.array([[ -4,  1,  0,  1,  0,  0,  0,  0,  0],[  1, -4,  1,  0,  1,  0,  0,  0,  0],[  0,  1, -4,  0,  0,  1,  0,  0,  0],[  1,  0,  0, -4,  1,  0,  1,  0,  0],[  0,  1,  0,  1, -4,  1,  0,  1,  0],[  0,  0,  1,  0,  1, -4,  0,  0,  1],[  0,  0,  0,  1,  0,  0, -4,  1,  0],[  0,  0,  0,  0,  1,  0,  1, -4,  1],[  0,  0,  0,  0,  0,  1,  0,  1, -4]],float)

b = np.array([-175, -75, -75, -100, 0, 0, -125, -25, -25], dtype=float)
D = np.diag(np.diag(A))
L = D - np.tril(A)
U = D - np.triu(A)
radio_jac = max(abs(np.linalg.eig(np.dot(np.linalg.inv(D), L+U))[0]))
print(radio_jac)
radio_gs = max(abs(np.linalg.eig(np.dot(np.linalg.inv(D-L), U))[0]))
print(radio_gs)
T, iters = sel.gauss_seidel_sumas(A, b, np.zeros(9), 1e-6)
print(T)
