from larch.xafs import feff6l
import matplotlib.pyplot as plt
import numpy as np

feff6l(folder='./feff',feffinp='feff.inp',verbose=False)

inputfile=open('./feff/chi.dat','r')
lines=inputfile.readlines()

_k=[];_chi=[]
for i in range(12,len(lines)):
    p=lines[i].split()
    _k.append(float(p[0]))
    _chi.append(float(p[1]))

k=np.zeros([int((20-0)/0.05+1),],dtype=float)
chi=np.zeros([int((20-0)/0.05+1),],dtype=float)

for i in range(0,len(k)):
    k[i]=_k[i]
    chi[i]=_chi[i]

plt.plot(k,chi*k**2)
plt.xlim([2,12])
plt.savefig('./feff/example.png')
