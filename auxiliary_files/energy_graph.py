import math
#import matplotlib.pyplot as plt
import os

ev_J = 1.60218e-19
hbar = 1.0545e-34
kB = 1.38064852e-23
cminv_radps = 2*math.pi*100*299792458 
tot_energy = 0
freq = []
eh_energy = []
ph_energy = []
e_temp = []
h_temp = []
h_energy_array = []
e_energy_array = []
tot_energy = 0
energy_band = []

file = open("..input/fermi_contents")
charges = (file.readline().split())[0]
file.close()

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

if (charges != 'e'):
    Hf = (input("Input the fermi energy for holes in eV"))
    while (not is_number(Hf)):
        Hf = (input("Input the fermi energy for holes in eV"))
    Hf = float(Hf)*ev_J

if (charges != 'h'):
    Ef = (input("Input the fermi energy for electrons in eV"))
    while (not is_number(Hf)):
        Ef = (input("Input the fermi energy for electrons in eV"))
    Ef = float(Ef)*ev_J

dvalues = open("d_values","r")
dvol_q = float(dvalues.readline().split()[1])
dvol_k = float(dvalues.readline().split()[1])
dvalues.close()


def df_FD(E,mu,temperature):
    if (abs((E-mu)/(kB*temperature))>20):
        return 0
    else:
        return math.exp((E-mu)/(kB*temperature))*(E-mu)/((math.exp((E-mu)/(kB*temperature))+1)*(math.exp((E-mu)/(kB*temperature))+1)*kB*temperature*temperature)

def calc_loss(ep, hp):
    eph_en_loss_e = 0
    eph_en_loss_h = 0
    for i in range(num_qpts):
        for j in range(num_bnds):
            eph_en_loss_e += hbar*freq[i][j]*ep[i][j]*dvol_q/(2*math.pi*2*math.pi*2*math.pi)
            eph_en_loss_h += hbar*freq[i][j]*hp[i][j]*dvol_q/(2*math.pi*2*math.pi*2*math.pi)
    #print(str(eph_en_loss_e) + " " + str(eph_en_loss_h)) 
    return eph_en_loss_e + eph_en_loss_h

def int_energy(freq, temp):
    freq = freq/(2*math.pi)
    x = (hbar*freq)/(kB*temp)
    return (((hbar*freq)/(math.exp(x)-1))+(freq*hbar/2))*dvol_q/(2*math.pi*2*math.pi*2*math.pi)

def holes_energy(F,temperature,num_kpts,num_e_bnds):
    C_h = 0
    for i in range(num_kpts):
        for j in range(num_e_bnds):
            C_h += (energy_band[i][j]-F)*df_FD(energy_band[i][j],F,temperature)*2*dvol_k/(2*math.pi*2*math.pi*2*math.pi)
    #print("holes " + str(temperature/C_h))
    return temperature*C_h

def electron_energy(F,temperature,num_kpts,num_e_bnds):
    C_e = 0
    for i in range(num_kpts):
        for j in range(num_e_bnds):
            C_e += (energy_band[i][j]-F)*df_FD(energy_band[i][j],F,temperature)*2*dvol_k/(2*math.pi*2*math.pi*2*math.pi)
    #print("electron " + str(temperature/C_e))
    return temperature*C_e

def read_temperatures():
    temp = open("T_e.txt","r")
    for lines in temp:
        line = lines.split()
        e_temp.append(float(line[1]))
        h_temp.append(float(line[2]))
    temp.close()

temp = open("../input/grid_info.txt","r")
num_qpts = int((temp.readline().split())[0])
num_bnds = int((temp.readline().split())[0])
temp.close()

energy = open("../input/band.eig","r")
values = energy.readline().split()
num_e_bnds = int(values[2].replace(',',''))
num_kpts = int(values[4])
count = 0
while True:
    energy.readline() #skip coordinates 
    values = energy.readline()
    energy_band.append([])
    if not values:
       break
    else:
       for value in values.split():
           energy_band[count].append(float(value)*ev_J)
    count += 1 
energy.close()

fre = open("../input/omegaq.freq","r")
fre.readline()
for i in range(num_qpts):
    fre.readline()
    freq.append([])
    values = fre.readline().split()
    for value in values:
        freq[i].append(float(value)*cminv_radps)

fre.close()

read_temperatures()

files = os.listdir("output_occ_change_ep")
files.sort(key=lambda f: int(os.path.splitext(f)[0]))
count = 0
energy_loss = 0
for those in files:
    occ_change_ep = []
    occ_change_hp = []
    for i in range(num_qpts):
        occ_change_ep.append([])
        occ_change_hp.append([])
    pt = 0
    ph_en = 0
    e = open("output_occ_change_ep/" + those,"r")
    h = open("output_occ_change_hp/" + those,"r")
    ph = open("output/" + those,"r")
    while True:
        e_values = e.readline().split()
        h_values = h.readline().split()
        ph_values = ph.readline().split()
        if not e_values:
           break
        else:
            for i in range(0,num_bnds*2,2):
                occ_change_ep[pt].append(float(e_values[i+1]))
                occ_change_hp[pt].append(float(h_values[i+1]))
                fre = float(ph_values[i])
                tem = float(ph_values[(i+1)])
                if math.isnan(tem):
                   continue
                ph_en += int_energy(fre,tem)
        pt += 1
    eh_energy.append(energy_loss)
    energy_loss += calc_loss(occ_change_ep, occ_change_hp)
    h_energy_array.append(holes_energy(Hf,h_temp[count],num_kpts,num_e_bnds))
    e_energy_array.append(electron_energy(Ef,e_temp[count],num_kpts,num_e_bnds))
    ph_energy.append(ph_en)
    e.close()
    h.close()
    ph.close()
    count += 1

en = open("energy_file", "w+")
en.write("Phonon Energy" + " " + "Charge Energy" + " " + "Total Energy")
for i in range(len(ph_energy)):
    tot_energy = h_energy_array[i] + e_energy_array[i]
    en.write(str(ph_energy[i]) + " " + str(tot_energy) + " " + str(tot_energy + ph_energy[i]))
    en.write("\n")
en.close()
