import matplotlib.pyplot as plt
import math
import re
import numpy as np; np.random.seed(0)
import matplotlib.colors
import pandas as pd

array = []
temp_array = []
path = []
index_array = []
hbar = 1.0545e-34
eV_J = 1.60217662e-19
J_eV = 1/eV_J
y_values = [0, 0]
temperatures = [0, 0]

def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		return False

file = open("../input/fermi_contents")
charges = (file.readline().split())[0]
file.close()

ph_filename = input("Input the phonon pathname")
time = (input("Please input the time of which you are modeling"))
while (not is_number(time)):
	time = (input("Please input the time of which you are modeling"))
time = float(time)

string = input('Please input an "(x1,y1) (x2,y2)" for your path ')
string = string.replace('(',' ')
string = string.replace(')',' ')
string = string.replace(',',' ')
values = string.split()
for i in range(2):
	path.append([])
	j = i*2
	path[i].append(values[j])
	path[i].append(values[j+1])
dec = input('Input further points? ("yes" or "no") ')
while (dec == 'yes'):
	string = input('Please input an "(x1,y1)" for your path ')
	string = string.replace('(',' ')
	string = string.replace(')',' ')
	string = string.replace(',',' ')
	values = string.split()
	i = len(path)
	path.append([])
	path[i].append(values[0])
	path[i].append(values[1])
	dec = input('Input further points? ("yes" or "no") ')
print(path)

left_bc = [-0.327653, 0.00000]
right_tc = [0.316709, 0.00000 ]
right_bc = [-0.005472, -0.560198]
left_tc = [0.00000, 0.559463]

def find_path_points(first,second,path_num):
	slope = (second[1] - first[1])/(second[0] - first[0])
	intercept = -slope*(first[0]) + first[1]
	#print(slope)
	#print(intercept)
	f = open("../input/omegaq.freq", "r")
	
	counter = 0

	skip = f.readline()

	while True:
		line = f.readline()
		if not line:
			break
		else:
			line = line.split()
			if (abs((slope*(float(line[0])) + intercept)-(float(line[1])))<0.02):
				#print(str(line[0]) + " " + str(line[1]))
				line = f.readline()
				for x in range(num_bnds):
					band = float((line.split())[x])
					band = band*0.12398
					if (band < y_values[0]):
						y_values[0] = band
					if (band > y_values[1]):
						y_values[1] = band
					array[path_num][x].append(band)
				index_array[path_num].append(counter)
				continue
			f.readline() ## skip the bands
			counter += 1

	f.close()


def get_temperatures():
	temp_file = open("T_e.txt","r")
	values = temp_file.readline().split()
	file_time = float(values[0])
	while (file_time != time):
		values = temp_file.readline().split()
		file_time = float(values[0])
	if (charges == 'e'):
		temperatures[1] = float(values[1])
	elif (charges == 'h'):
		temperatures[0] = float(values[1])
	else:
		temperatures[1] = float(values[2])
		temperatures[0] = float(values[1])
	temp_file.close()

def band_graph():

	displacement = 0
	let_cnt = 1
	locs = []
	labels = []

	cmap = plt.cm.rainbow
	norm = matplotlib.colors.Normalize(vmin=400, vmax=850)

	props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

	fig, ax = plt.subplots()

	locs.append(0)
	labels.append("A")

	xmin, xmax = plt.xlim()
	ymin, ymax  = plt.ylim()

	plt.ylim(ymin=y_values[0])
	plt.ylim(ymax=y_values[1])

	plt.xlim(xmin=0)


	for p in range(paths):
		x = list(range(displacement,displacement+len(array[p][0])))
		displacement += len(array[p][0])
		locs.append(displacement)
		labels.append(chr(ord('A')+let_cnt))
		let_cnt += 1
		print(displacement)
		for i in range(num_bnds):
			df = pd.DataFrame({"x":x,"y":array[p][i]})
			ax.scatter(df.x, df.y, color=cmap(norm(temp_array[p][i])));

		#plt.hold()

	plt.xlim(xmax=displacement)
	sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
	sm.set_array([])
	fig.colorbar(sm)

	
	if (charges == 'b'):
		ax.text(0.01,0.99,"T=" + str(time) + ", T_e=" + str(temperatures[1]) + ", T_h=" + str(temperature[0]),  transform=ax.transAxes, fontsize=6, verticalalignment='top', bbox=props)
	if (charges == 'e'):
		ax.text(0.01,0.99,"T=" + str(time) + ", T_e=" + str(temperatures[1]),  transform=ax.transAxes, fontsize=6, verticalalignment='top', bbox=props)
	if (charges == 'h'):
		ax.text(0.01,0.99,"T=" + str(time) + ", T_h=" + str(temperatures[0]),  transform=ax.transAxes, fontsize=6, verticalalignment='top', bbox=props)

	plt.xticks(locs,labels)
	plt.ylabel("Phonon Energy (meV)")
	plt.show()


f = open("../input/omegaq.freq", "r")

values = f.readline().split()
num_bnds = int(values[2].replace(',',''))
num_qpts = int(values[3][4:])

paths = len(path)-1

for p in range(paths):
	array.append([])
	index_array.append([])
	temp_array.append([])
	for x in range(num_bnds):
		array[p].append([])
		temp_array[p].append([])

f.close()

for p in range(paths):
	find_path_points(path[p],path[p+1],p)


m = open(ph_filename, "r")
content = m.readlines()
for p in range(paths):
	length = len(index_array[p])
	for i in range(length):
		index = index_array[p][i]
		values = content[index].split()
		for i in range(1,len(values),2):
			temp = float(values[i])
			#print(temp)
			index = int(i/2)
			temp_array[p][index].append(temp)


get_temperatures()
band_graph()
