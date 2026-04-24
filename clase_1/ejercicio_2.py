def suma(n):
  s=0
  for i in range(1,n+1):
    s+=1/i**2
  return s

print(f'la suma da como resultado {suma(20)}')