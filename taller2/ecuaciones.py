import numpy as np
import matplotlib.pyplot as plt

def Euler(f, a, b, h, co):
    n = int((b-a) / h)
    y_euler = [co]

    for i in range(n):
        y_euler.append(y_euler[i]+h*f(a+i*h, y_euler[i]))
    return np.linspace(a, b, n+1), y_euler

def f(t, y):
    w = y[0]
    z = y[1]
    f1 = z
    f2 = t*np.exp(2*t) - 6*z - 9*w
    return np.array([f1, f2])

t, sol = Euler(f, 0, 1, 0.25, np.array([0, 1]))
y_sol = np.array(sol)[:,0]
y_prime = np.array(sol)[:,1]

# print(t)
# print(sol)
print(y_sol)
print(y_prime)
