import matplotlib.pyplot as plt
import math
import urllib.request
import os


# 0.28 charges for -3.6

array = []

title = input("Please input the compound name")

def band_graph(array):
	for band in array:
		plt.plot(band)
		plt.hold(True)
	plt.xlabel("kpts")
	plt.ylabel("Energy (eV)")
	plt.title(title + " " + "Bandstructure")
	plt.show()

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

band_graph(array)

