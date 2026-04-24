import numpy as np

perimetro = lambda r: 2*np.pi*r

print(f'El perimetro de un circulo es {perimetro(5)}')

def perimetro_2(r):
  return 2*np.pi*r

print(f'El perimetro de un circulo es {perimetro_2(5)}')