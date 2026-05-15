import numpy as np
import matplotlib.pyplot as plt

# Para resolver el problema y´=f(t,y)
def Euler(f, a, b, h, co):
    n = int((b-a) / h)
    y_euler = [co]

    for i in range(n):
        y_euler.append(y_euler[i]+h*f(a+i*h, y_euler[i]))
    return np.linspace(a, b, n+1), y_euler
