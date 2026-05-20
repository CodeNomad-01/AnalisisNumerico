import ecuaciones as edo
import numpy as np
import matplotlib.pyplot as plt

# El estudio de modelos matemáticos para predecir la dinámica de una población de especies competentes tiene 
# su origen en los trabajos independientes publicados en la primera época del siglo xx por A. J. Lotka y V. Volterra 

# Considere el problema de predecir la población de dos especies, una de las cuales es un depredador, cuya población 
# en el tiempo $t$ es $x_2(t)$, que se alimenta de la otra, que es la presa, cuya población es $x_1(t)$. Supondremos 
# que la presa siempre tiene un suministro de comida adecuado y que su índice de natalidad en cualquier tiempo es 
# proporcional al número de presas vivas en ese momento; es decir, el índice de natalidad (presa) es $k_1x_1(t)$.
#  El índice de mortalidad de la presa depende tanto del número de presas como de depredadores vivos en ese momento. 
# Para simplicidad, suponemos un índice de mortalidad (presa) $=k_2x_1(t)x_2(t)$. El índice de natalidad del depredador, 
# por otro lado, depende de su suministro de comida, $x_1(t)$, así como del número de depredadores disponible para propósitos 
# de reproducción. Por esta razón, suponemos que el índice de natalidad (depredador) es $k_3x_1(t)x_2(t)$. El índice de mortalidad 
# del depredador será tomado como simplemente proporcional al número de depredadores vivos en ese momento; es decir, el índice de 
# mortalidad (depredador) $= k_4x_2(t)$.\\
# Puesto que $x_1(t)$ y $x_2(t)$ representan el cambio en las poblaciones de presas y depredadores, respectivamente, 
# en relación con el tiempo, el problema se expresa mediante el sistema de ecuaciones diferenciales no lineales

# $$
# x'_1(t) = k_1x_1(t) - k_2x_1(t)x_2(t) \\
# x'_2(t) = k_3x_1(t)x_2(t) - k_4x_2(t)
# $$
# Resuelva este sistema para $0 \leqslant t \leqslant 4$, al suponer que la población inicial de la presa es 1000 y que 
# la del depredador es 500 y que las constantes son $k_1 = 3$, $k_2 = 0.002$, $k_3 = 0.0006$, y $k_4 = 0.5$. Bosqueje una 
# gráfica de las soluciones para este problema, al graficar ambas poblaciones con el tiempo y describa el fenómeno físico 
# representado. ¿Existe una solución estable para este modelo de población? En caso afirmativo, ¿Para qué valores de $x_1$ y $x_2$ 
# la solución es estable?


def competencia(t, y):
    # Y = [presa, depredador]
    x1 = y[0]
    x2 = y[1]
    k1 = 3
    k2 = 0.002
    k3 = 0.0006
    k4 = 0.5
    f1 = k1*x1 - k2*x1*x2
    f2 = k3*x1*x2 - k4*x2
    return np.array([f1, f2])

t, sol = edo.Euler(competencia, 0, 20, 0.001, np.array([1000, 500]))
presa = np.array(sol)[:,0]
depredador = np.array(sol)[:,1]

print(presa)
print(depredador)

plt.subplot(121)
plt.plot(t, presa, 'b-', label='Presa')
plt.plot(t, depredador, 'r-', label='Depredador')
plt.legend()
plt.xlabel('Tiempo')
plt.ylabel('Población')
plt.title('Competencia entre presa y depredador')
plt.grid()

plt.subplot(122)
plt.plot(presa, depredador, 'g-', label='Competencia')
plt.legend()
plt.xlabel('Población de presa')
plt.ylabel('Población de depredador')
plt.title('Competencia entre presa y depredador')
plt.grid()
plt.show()
