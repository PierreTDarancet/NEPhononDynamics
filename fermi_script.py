import matplotlib.pyplot as plt
import math
import urllib.request
import os


array = []
masses = []
con_band = 0
val_band = 0
Fermi = 0
Ef = 0
Hf = 0
E_bnd_min = 0
E_bnd_max = 0
H_bnd_min = 0
H_bnd_max = 0
Efsthick = 1.2
Hfsthick = 1.2
val_electrons = 0
sumq = 0
emin = 0
emax = 0
error = 0.001
kB = 1.3806e-23
J_ev = 6.242e18
kT = 3000*kB*J_ev

def get_valence(array):
	a_num = 0
	temp = 0
	for ele_num in range(len(array)):
		file_name = (array[ele_num]).replace("upf", "UPF")
		v = urllib.request.urlopen("http://nninc.cnf.cornell.edu/psp_files/" + file_name)
		for line in v:
			split = line.split()
			if (not split or len(split) <= 2):
				continue
			if (b'valence' in split[2]):
				temp = int(float(split[0]))
				break
		a_num = temp + a_num
		v.close()
	return a_num

def fermi_step(e, ef):
	val = (e-ef)/kT
	if (val > 100):
		return 0
	elif (val < -100):
		return 1
	return (1.0/(1.0+math.exp(val)))


def fermi_integrate(num_kpts, num_bnds, Ef, set_low=None, set_high=None):
	sumq = 0.0
	chunk = 1.0/num_kpts
	for i in range(num_bnds):
		for j in range(num_kpts):
			if (set_low != None and array[i][j] < set_low):
				continue
			if (set_high != None and array[i][j] > set_high):
				continue
			E = array[i][j]
			sumq = sumq + fermi_step(E, Ef)*2.0*chunk
			if (E >= (Ef + 5*kT)):
				return sumq
	return sumq


for file in os.listdir(os.curdir):
	if file.endswith(".in"):
		input_file = file
m = open(input_file, "r")
num_ele = 0
psuedo_files = []
while True:
	line = m.readline().split()
	if not line:
		continue
	if (line[0] == "ntyp"):
		nat = int(line[2].replace(',',''))
	if (line[0] == "ATOMIC_SPECIES"):
		break

cnt = 0

while True:
	if (cnt == nat):
		break
	line = m.readline().split()
	if not line:
		continue
	psuedo_files.append(line[2])
	cnt += 1
val_electrons = get_valence(psuedo_files)
m.close()

<<<<<<< HEAD
=======
m = open("masses.txt", "r")
while True:
	mass = m.readline()
	if not mass:
		break
	else:
		temp = float((mass.split())[0])
		masses.append(temp)
val_electrons = get_valence(masses)
m.close()
>>>>>>> 129a52cc6d50c765929df240a361e3b20db478ea

f = open("band.eig", "r")
values = f.readline()
i = 0
for words in values.split():
	i += 1
	if (i == 3):
		num_bnds = words
	if (i == 5):
		num_kpts = words
		num_kpts = int(num_kpts)

num_bnds = int(num_bnds.replace(',',''))

chunk = 1.0/num_kpts

for x in range(num_bnds):
	array.append([])

while True:
	f.readline() ## skip the k_pt
	line = f.readline()
	if not line:
		break
	else:
		for x in range(num_bnds):
		  band = float((line.split())[x])
		  array[x].append(band)

emin_abs = min(array[0])
emax_abs = max(array[num_bnds-1])

emin = emin_abs
emax = emax_abs

for run in range(50):
	Fermi = 0.5*(emin+emax)
	sumq = 0.0
	sumq = fermi_integrate(num_kpts, num_bnds, Fermi)
	if (abs(sumq-val_electrons) < error):
		break
	elif (sumq < val_electrons):
		emin = Fermi
	else:
		emax = Fermi

## Add up all the states above the fermi energy
sumq = fermi_integrate(num_kpts, num_bnds, Fermi, set_low=Fermi)
sum_e = sumq

emin = emin_abs
emax = Fermi

for run in range(100):
	Hf = 0.5*(emin+emax)
	sumq = 0.0
	sumq = fermi_integrate(num_kpts, num_bnds, Hf)
	if (abs(sumq-(val_electrons-sum_e)) < error):
		break
	elif (sumq < (val_electrons-sum_e)):
		emin = Hf
	else:
		emax = Hf


emin = Fermi
emax = emax_abs

for run in range(100):
	Ef = 0.5*(emin+emax)
	sumq = 0.0
	sumq = fermi_integrate(num_kpts, num_bnds, Ef)
	if (abs(sumq-(val_electrons+sum_e)) < error):
		break
	elif (sumq < (val_electrons+sum_e)):
		emin = Ef
	else:
		emax = Ef

## Find conduction and valence bands
mini = 100
for i in range(num_bnds):
	diff = abs(min(array[i])-Ef)
	if (diff < mini):
		con_band = i+1
		val_band = i
		mini = diff

## bnd_min and bnd_max for electrons and holes
E_bnd_min = val_band
E_bnd_max = con_band+1
H_bnd_min = val_band-1
H_bnd_max = val_band+1

c = open('fermi_contents', 'w+')

c.write("Ef\n")
c.write(str(Ef) + "\n")
c.write("E_bnd_min\n")
c.write(str(E_bnd_min) + "\n")
c.write("E_bnd_max\n")
c.write(str(E_bnd_max) + "\n")
c.write("Efsthick\n")
c.write(str(Efsthick) + "\n")

c.write("Hf\n")
c.write(str(Hf) + "\n")
c.write("H_bnd_min\n")
c.write(str(H_bnd_min) + "\n")
c.write("H_bnd_max\n")
c.write(str(H_bnd_max) + "\n")
c.write("Hfsthick\n")
c.write(str(Efsthick) + "\n")

f.close()
c.close()



