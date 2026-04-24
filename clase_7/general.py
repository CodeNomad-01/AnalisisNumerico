import numpy as np
import sympy as sp

x = 35
y0 = 3
y = 1
g = 9.8
v0 = 20

f = lambda theta: (x*(np.tan(theta))) - (g*x**2)/(2*v0**2*np.cos(theta)**2) + y0 - y

print('Biseccion')
p = Biseccion(f, 0, np.pi/4, 1e-6)
print(f'El angulo inicial con el cual el lanzador tira la pelota es:{np.degrees(p)}')
print('')

print('Posicion Falsa')
c = PosicionFalsa(f, 0, np.pi/4, 1e-6)
print(f'El angulo inicial de la pelota es:{np.degrees(c)}')

x = sp.symbols('x')
x0 = 1
tol = 10**(-6)

f = x**2-8


Newton(f, x0, tol)

g = 9.78
mu = 5.14
L =  4.15
v = 17


f = g + (0.5*mu*v**2)/(mu*(L-x)+2*L)

a, b = Newton(f, 8, 1e-6 )
print(a, b)