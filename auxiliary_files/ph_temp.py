import os
import math
#from decimal import Decimal

hbar = 1.0545e-34
kB = 1.38064852e-23

def int_energy(freq, temp):
    freq = freq/(2*math.pi)
    x = (hbar*freq)/(kB*temp)
    return ((hbar*freq)/(math.exp(x)-1))+(hbar*freq/2)

def heat_cap(freq, temp):
    freq = freq/(2*math.pi)
    x = (hbar*freq)/(kB*temp)
    return kB*((x**2)*math.exp(x))/((math.exp(x)-1)**2)

write_to = open("T_Ph.txt","w+")
con = 10**10
counter = 0
files = os.listdir("output")
files.sort(key=lambda f: int(os.path.splitext(f)[0]))
for those in files:
    num = 0
    dem = 0
    f = open("output/" + those,"r")
    for lines in f:
        line = lines.split()
        for i in range(0,12,2):
            fre = float(line[i])
            tem = float(line[(i+1)])
            if math.isnan(tem):
               continue
            num = num + int_energy(fre,tem)
            dem = dem + heat_cap(fre,tem)
    #print(num)
    #print(dem)
    avg = num/dem
    write_to.write(str(counter/2000.0) + " " + str(avg))
    write_to.write("\n")
    f.close()
    if (counter < 3000):
        counter += 40
    else:
        counter += 200
#print(counter)                 
