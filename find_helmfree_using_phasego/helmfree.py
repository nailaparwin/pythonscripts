#####################################################
# calculate helmfree energy
# extracted and customized code from phasego
####################################################

import copy
import numpy as np
from scipy import integrate
import re

Formula_Name = 'CaO'
Names_of_Strs = 'fcc'
VE_data_File_Name = 've-0'
Units_VE = ["Bohr3", "Hartree"]
Ph_Dos_File_Base_Name = 'dos-'
#Tdata_Read = 0 2000 10
Unit_of_Freq = 'Ha'
# Some constants
ry = 13.6058
R = 8.314472                    # J / (mol*K)
h = 6.62606876e-34 * 2.99792458e10   # not hbar
kb = 1.3806504e-23              # J/K
e0 = 1.602176462e-19
NA = 6.02214199e23              # 1/mol
free_t = {}



tdata = np.arange(0, 2010, 10)
print(tdata)
num_formula_units = 1
inppath = 'inp-fcc-CaO'
outdir = './'


def parse_ve(vefile):
    ve_file = open(vefile, "r")
    vvee = {}

    lines = ve_file.readlines()

    for l in lines:
        line = l.strip().split()
        # The lines contained no numerical data in the first two columns are ignored
        if len(line) >= 2:
            try:
                line0 = float(line[0])
                line1 = float(line[1])
            except:
                pass

            else:
                vvee[line0] = line1

    vsort_tmp = vvee.keys()
    vsort=[]
    for i in vsort_tmp:
        vsort.append(i)
    vsort.sort()
    vsort.reverse()

    if Units_VE[0] == 'Bohr3':
        v_conv = 1.0
    elif Units_VE[0] == 'A3':
        v_conv = 1 / 0.529177**3.0

    if Units_VE[1] == 'Ry':
        e_conv = 1.0
    elif Units_VE[1] == 'Hartree':
        e_conv = 2.0
    elif Units_VE[1] == 'eV':
        e_conv = 2 / 27.21138

    ve = np.array([[i * v_conv, vvee[i] * e_conv] for i in vsort])

    ve_file.close()

    return ve


def name_parse(Name):
    chemical_symbols = ['X', 'H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F',
                       'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K',
                       'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu',
                       'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y',
                       'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In',
                       'Sn', 'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr',
                       'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm',
                       'Yb', 'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au',
                       'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac',
                       'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es',
                       'Fm', 'Md', 'No', 'Lr']

    tuple_list = re.findall(r'([A-Z][a-z]*|[a-z][a-z]*)(\d*)', Name)
    # print (tuple_list)
    name_dict = {}
    for i in tuple_list:
        if i[0].capitalize() in chemical_symbols:
            if i[1]:
                name_dict[i[0].capitalize()] = int(i[1])
            else:
                name_dict[i[0].capitalize()] = 1
        else:
            print ("Something in Formula_Name cannot be parsed. Please check!!!")
            exit(0)
    # print (name_dict)

    return name_dict

ve = parse_ve("ve-0")
free_t = np.zeros(shape=(len(ve), len(tdata), 2))
filehelmfree_v = open(outdir + "/tf.dat", "w")
filehelmfree_v.write("# T (K)" + 15 * " " + "Helmholtz Free Energy (Ry.)\n")

if Units_VE[0] == 'Bohr3':
    v_conv = 1.0
elif Units_VE[0] == 'A3':
    v_conv = 1 / 0.529177 ** 3.0


for n in range(len(ve)):
    filehelmfree_v.write("# V= %17.13f\n" % ve[n][0])
    phdos = np.loadtxt(inppath + "/%s%.4f-%s" % (Ph_Dos_File_Base_Name, ve[n][0]/v_conv,0))
    

    #print(phdos) #contains dos file data
    if Unit_of_Freq == 'cm-1':
        freq = copy.deepcopy(phdos[:, 0])
        dos = copy.deepcopy(phdos[:, 1])

    if Unit_of_Freq == 'THz':
        freq = copy.deepcopy(phdos[:, 0]) * 33.3564
        dos = copy.deepcopy(phdos[:, 1]) / 33.3564

    if Unit_of_Freq == 'meV':
        freq = copy.deepcopy(phdos[:, 0]) * 8.065541
        dos = copy.deepcopy(phdos[:, 1]) / 8.065541

    if Unit_of_Freq == 'eV':
        freq = copy.deepcopy(phdos[:, 0]) * 8065.541
        dos = copy.deepcopy(phdos[:, 1]) / 8065.541

    if Unit_of_Freq == 'Ha':
        freq = copy.deepcopy(phdos[:, 0]) * 219476.2755
        dos = copy.deepcopy(phdos[:, 1]) / 219476.2755

        integral = integrate.simps(dos, freq)

        #total densities of states are normalized to integral g(w)dw = 3nN ----------equation 8
        if int(round(integral)) == 1:
            # change to 3*num_formula_units*Num_Atoms for PHON code in which dos is normalized to 1.0.
            Formula_Name_dict = name_parse(Formula_Name)
            num_atoms = sum(Formula_Name_dict.values())
            # print num_atoms
            dos *= 3 * num_formula_units * num_atoms
            print("Formula_Name_dict ", Formula_Name_dict)
            print("num_atoms ", num_atoms)
            print("dos ", dos)

        for nT, T in enumerate(tdata):

            if T == 0:
               T = 10

            #??????????????????????????
            for i, f in enumerate(freq):
                if f < 1.5 * 2.2e-16:
                    freq[i] = 0.001
                    dos[i] = 0



            ########################################
            # F (V, T ) = E static (V ) + F el (V, T ) + F zp (V, T ) + F ph (V, T ) --------------eq(4)
            # F latt = F zp + F ph ,                                                ---------------eq(5)
            # calculate F latt - We can ignore F el for low temperatures            ---------------eq(6)
            ########################################

            # free energy:
            y1 = 0.5 * h * freq * dos + kb * T * np.log(2.0 * np.sinh(h * freq / (2.0 * kb * T))) * dos
            f_t = integrate.trapz(y1, freq) / e0 / ry
            print (T,f_t)
            if T == 10:
                T = 0

               
            free_t[n][nT] = [T, ve[n][1] / num_formula_units + f_t / num_formula_units]

            filehelmfree_v.write("%8.2f%22.13f\n" % (free_t[n][nT][0], free_t[n][nT][1]))

