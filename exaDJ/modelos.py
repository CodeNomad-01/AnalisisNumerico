import numpy as np
import sympy as sp
import sel as sl
import matplotlib.pyplot as plt

x = sp.symbols('x')

def Matriz(x_data):
    n=len(x_data)
    A=np.zeros([n,n], float)
    A[0:n,0]=1
    for j in range(1,n):
        for i in range(n):
            A[i,j]=A[i,j-1]*x_data[i]
    return A

def Lagrange(x_data, y_data):
    n = len(x_data)

    Polinomio = 0

    for i in range(n):
        Li = 1
        for j in range(n):
            if j != i:
                Li *= (x - x_data[j])/(x_data[i]-x_data[j])
        Polinomio += Li * y_data[i]
    return sp.expand(Polinomio)

def Polinomial_simple(x_data, y_data):
    n = len(x_data)
    A = Matriz(x_data)
    coef = sl.eliminacion_gaussiana_pivoteo(A, y_data)
    P = sum(coef[i]*x**i for i in range(n))
    return P

def minimos_cuadrados(x_data, y_data):
    n = len(x_data)
    Sx = sum(x_data)
    Sy = sum(y_data)
    Syx = sum(y_data * x_data)
    Sx2 = sum(x_data ** 2)

    m = (n * Syx - Sy * Sx) / (n * Sx2 - Sx ** 2)
    b = (Sy * Sx2 - Sx * Syx) / (n * Sx2 - Sx ** 2)

    return m, b

def coeficiente_determinacion(x, y):
    n = len(x)
    ybar = sum(y) / n
    m, b = minimos_cuadrados(x, y)
    y_gorro = lambda x: m * x + b
    numerador = sum((y - y_gorro(x)) ** 2)
    denominador = sum((y - ybar) ** 2)
    R2 = 1 - numerador / denominador
    return R2

def construir_placa(filas, columnas, t_arriba, t_abajo, t_izq, t_der):
    n = filas * columnas
    A = np.zeros((n, n))
    b = np.zeros(n)

    for fila in range(filas):
        for col in range(columnas):
            k = fila * columnas + col
            A[k, k] = 4
            if col > 0:              A[k, k - 1] = -1
            else:                    b[k] += t_izq
            if col < columnas - 1:   A[k, k + 1] = -1
            else:                    b[k] += t_der
            if fila > 0:             A[k, k - columnas] = -1
            else:                    b[k] += t_abajo
            if fila < filas - 1:     A[k, k + columnas] = -1
            else:                    b[k] += t_arriba

    return A, b

def escalas(xd,yd):
    plt.figure(figsize = (12,12), dpi = 80)
    plt.suptitle('Escalas de transformacion', fontsize = 14, fontweight = 'bold')
    
    #-----------------------------------------------
    plt.subplot(331)
    plt.scatter(xd, yd, color = 'red', label = 'Datos originales')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid()
    plt.legend()
    plt.title('Datos originales', fontsize = 10, fontweight = 'bold')
    
    #-----------------------------------------------
    plt.subplot(332)
    plt.scatter(xd**2, yd, color = 'blue', label = '$x^2$')
    plt.xlabel('$x^2$')
    plt.ylabel('y')
    plt.grid()
    plt.legend()
    plt.title('Transformación $x^2$', fontsize = 10, fontweight = 'bold')
    
    #-----------------------------------------------
    plt.subplot(333)
    plt.scatter(xd**3, yd, color = 'magenta', label = '$x^3$')
    plt.xlabel('$x^3$')
    plt.ylabel('y')
    plt.grid()
    plt.legend()
    plt.title('Transformación $x^3$', fontsize = 10, fontweight = 'bold')
    
    #-----------------------------------------------
    plt.subplot(334)
    plt.scatter(xd, 1/yd, color = 'purple', label = r'$\frac{1}{y}$')
    plt.xlabel('x')
    plt.ylabel(r'$\frac{1}{y}$')
    plt.grid()
    plt.legend()
    plt.title(r'Transformación $\frac{1}{y}$', fontsize = 10, fontweight = 'bold')
    
    #-----------------------------------------------
    plt.subplot(335)
    plt.scatter(xd, np.log(yd), color = 'black', label = r'$log(y)$')
    plt.xlabel('x')
    plt.ylabel(r'$log(y)$')
    plt.grid()
    plt.legend()
    plt.title(r'Transformación $log(y)$', fontsize = 10, fontweight = 'bold')
    
    #-----------------------------------------------
    plt.subplot(336)
    plt.scatter(xd, np.sqrt(yd), color = 'brown', label = r'$\sqrt{y}$')
    plt.xlabel('x')
    plt.ylabel(r'$\sqrt{y}$')
    plt.grid()
    plt.legend()
    plt.title(r'Transformación $\sqrt{y}$', fontsize = 10, fontweight = 'bold')
    
    #-----------------------------------------------
    plt.subplot(337)
    plt.scatter(np.log(xd), yd, color = 'orange', label = '$log(x)$')
    plt.xlabel('$log(x)$')
    plt.ylabel('y')
    plt.grid()
    plt.legend()
    plt.title(r'Transformación $log(x)$', fontsize = 10, fontweight = 'bold')
    
    #-----------------------------------------------
    plt.subplot(338)
    plt.scatter(np.log(xd), np.log(yd), color = 'cyan', label = '$log(x)$ - $log(y)$')
    plt.xlabel('$log(x)$')
    plt.ylabel('$log(y)$')
    plt.grid()
    plt.legend()
    plt.title(r'Transformación $log(x)$ - $log(y)$', fontsize = 10, fontweight = 'bold')
    
    #-----------------------------------------------
    plt.subplot(339)
    plt.scatter(np.sqrt(xd), yd, color = 'green', label = r'$\sqrt{x}$')
    plt.xlabel(r'$\sqrt{x}$')
    plt.ylabel('y')
    plt.grid()
    plt.legend()
    plt.title(r'Transformación $\sqrt{x}$', fontsize = 10, fontweight = 'bold')

    plt.subplots_adjust(top = 0.93, bottom = 0.06, left = 0.07, right = 0.97, hspace = 0.55, wspace = 0.35)
    return