import matplotlib.pyplot as plt
import math

file = open("../input/fermi_contents")
charges = (file.readline().split())[0]
file.close()

f = open("T_e.txt", "r")
x_array = []
y1_array = []
y2_array = []
for line in f:
    line = line.split()
    if (float(line[0]) == 0):
    	continue
    x_array.append((float(line[0])))
    y1_array.append(math.log(float(line[1])))
    if (len(line) > 2):
        y2_array.append(math.log(float(line[2])))
if (charges[0] == 'h'):
    plt.plot(x_array,y1_array,label='Holes')
else:
    plt.plot(x_array,y1_array,label='Electrons')
plt.hold(True)
if (len(y2_array) != 0):
   plt.plot(x_array,y2_array,label='Holes')

f.close()

ph = open("T_Ph.txt", "r")
y_array = []
for line in ph:
	 line = line.split()
	 y_array.append(math.log(float(line[1])))
plt.plot(x_array,y_array,label='Phonons',color='green')

ph.close() 

plt.title("Temperature Change of Electrons and Phonons")
plt.ylabel("Log(Temp) (K)")
plt.xlabel("Time (ps)")
plt.legend(loc='upper right')
plt.show()




    
