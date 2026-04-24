import numpy as np
import matplotlib.pyplot as plt

x = np.arange(0,4,0.5) #args=pto inicial, punto final, espaciamiento
xx = np.linspace(0,4,1000) #args=pto inicial, punto final, cantidad de puntos

y = np.exp(-xx)*np.sin(2*np.pi*xx)
# print(y, type(y), len(y))
plt.plot(xx,y)

plt.ylim(-0.2,0.2)
