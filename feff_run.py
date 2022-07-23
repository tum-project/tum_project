from larch.xafs import feff8l
import matplotlib.pyplot as plt
import numpy as np

feff8l(folder='./feff',feffinp='feff.inp',verbose=False)

inputfile=open('./feff/chi.dat','r')
lines = inputfile.read().strip().split("\n")

_k=[];_chi=[]
for i in range(14,len(lines)):
    p=lines[i].split()
    _k.append(float(p[0]))
    _chi.append(float(p[1]))

k=np.array(_k,dtype=float)
chi=np.array(_chi,dtype=float)

# for i in range(0,len(k)):
#     k[i]=_k[i]
#     chi[i]=_chi[i]

plt.plot(k,chi*k**2)
plt.xlim([2,12])
plt.savefig('./feff/example.png')
