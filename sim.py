"""
Août 2020
ENSMR - Dep Info, MSIP
Mini projet Simulation
----------------------
• Abdelaziz Saroui
• Amina Ait Aziz
• Abdessamad Jalal
• Ikram Zitou
"""

from math import sqrt

# Importation de Pandas, utilisé pour générer les fichiers excel à partir des données
try:
	import pandas as pd
	pand = True
except:
	print("Le programme de simulation nécessite le module Pandas pour la génération des fichiers Excel!")
	print("Vous pouvez l'installer avec : pip install pandas \n")
	pand = False

SN = 0
while SN not in (1, 2, 3):
	print("\n→ Choisir le scénario de la simulation:")
	print("1 : Scénario 1")
	print("2 : Scénario 2")
	print("3 : Scénario 3")
	SN = int(input())
if SN == 1:
	print("\n----- Scénario 1 -----")
elif SN == 2:
	print("\n----- Scénario 2 -----")
elif SN == 3:
	print("\n----- Scénario 3 -----")

def gen_alea(x, y, z):
	"""
	Génèration un nombre aléatoire entre 0 et 1
	"""
	x = 171 * (x % 177) - 2 * (x // 177)
	y = 172 * (y % 176) - 35 * (y // 176)
	z = 170 * (z % 178) - 63 * (z // 178)
	if (x < 0):
 		x = x + 30269
	if (y < 0):
 		y = y + 30307
	if (z < 0): 
 		z = z + 30323
	inter = ((x / 30269) + (y / 30307) + (z / 30232))
	return inter - int(inter)

def val_unif(a, b, P):
	"""
	Calcul de la valeur d'une variable aléatoire pour la loi uniforme
	a, b : les bornes de l'intervalle
	P : pourcentage de réduction de l'intervalle (P=0.1 pour le scénario 2)
	"""
	if SN == 2 or SN == 3:
		if a < 0:
			a = a + a * P
		else:
			a = a - a * P
		if b < 0:
			b = b + b * P
		else:
			b = b - b * P
	return (b - a) * alea + a


def ntac(ntac_pre, alea, alea_ntac):
	"""
	Calcul de NTAC, le nombre total d’accidents corporels
	ntac_pre : le NTAC de l'année précedente
	alea, alea_ntac : nombres aléatoires entre 0 et 1
	"""
	if alea_ntac <= 0.1:
		a = -0.03
		b = 0
	elif alea_ntac <= 0.37:
		a = 0
		b = 0.02
	elif alea_ntac <= 0.64:
		a = 0.02
		b = 0.04
	elif alea_ntac <= 0.78:
		a = 0.04
		b = 0.07
	elif alea_ntac <= 0.92:
		a = 0.07
		b = 0.11
	else:
		a = 0.11
		b = 0.14

	x = val_unif(a, b, P)
	return int(ntac_pre * (1 + x))

def ntam(ntac, ntac_pre, ntam_pre, alea, alea_ntam):
	"""
	Calcul de NTAM, le nombre total d’accidents mortels
	ntac : le NTAC de la même année
	ntac_pre : le NTAC de l'année précedente
	ntam_pre : le NTAM de l'année précedente
	alea, alea_ntam : nombres aléatoires entre 0 et 1
	"""
	if alea_ntam <= 0.2:
		a = -0.0045
		b = -0.0025
	else:
		a = -0.0025
		b = 0

	x = val_unif(a, b, P)
	taux = ntam_pre / ntac_pre + x
	return int(taux * ntac)

def ntanm(ntac, ntam):
	"""
	Calcul de NTANM, le nombre total d’accidents non mortels
	ntac : le NTAC de la même année
	ntam : le NTAM de la même année
	"""
	return ntac - ntam

def ntt(ntam, ntt_pre, ntam_pre, alea):
	"""
	Calcul de NTT, le nombre total de tués de la route
	ntam : le NTAM de la même année
	ntt_pre : le NTT de l'année précedente
	ntam_pre : le NTAM de l'année précedente
	alea : nombre aléatoire entre 0 et 1
	"""
	a = -0.03
	b = 0.015

	x = val_unif(a, b, P)
	taux = ntt_pre / ntam_pre + x
	return int(taux * ntam)


def ntb(ntac, ntb_pre, ntac_pre, alea):
	"""
	Calcul de NTB, le nombre total de blessés
	ntac : le NTAC de la même année
	ntb_pre : le NTB de de l'année précedente
	alea : nombre aléatoire entre 0 et 1
	"""
	a = -0.04
	b = 0.01

	x = val_unif(a, b, P)
	taux = ntb_pre / ntac_pre + x
	return int(taux * ntac)

def ntbg(ntb, alea):
	"""
	Calcul de NTBG, le nombre total de blessés graves
	ntb : le NTB de la même année
	alea : nombre aléatoire entre 0 et 1
	"""
	a = 0.04
	b = 0.09

	x = val_unif(a, b, P)
	return int(x * ntb)

def ntbl(ntb, ntbg):
	"""
	Calcul de NTBL, le nombre total de blessés légers
	ntb : le NTB de la même année
	ntbg : le NTBG de la même année
	"""
	return ntb - ntbg

def nmtj(ntt):
	"""
	Calcul de NMTJ, le nombre moyen de tués de la route par jour
	ntt : le NTT de la même année
	"""
	return round(ntt / 365, 2)


# Années de début et de fin de la simulation
debut = 2018
fin = int(input("\n→ Entrer l'année de fin ( Année de début est 2018 ): \n"))

# Nombre de simulations
N = int(input("\n→ Entrer le nombre de simulations: \n"))

# La valeur des germes pour la fonction gen_alea
print("\n→ Initialiser les germes de la fonction Alea:")
germes = [0 for i in range(9)]

# Germes pour alea utilisé dans tous les indicateurs
germes[0] = int(input("IX = "))
germes[1] = int(input("IY = "))
germes[2] = int(input("IZ = "))

# Germes pour la loi tabulée de NTAC
germes[3] = germes[0] + 31
germes[4] = germes[1] + 31
germes[5] = germes[2] + 31

# Germes pour la loi tabulée de NTAM
germes[6] = germes[0] + 48
germes[7] = germes[1] + 48
germes[8] = germes[2] + 48

# Initialisation du dictionnaire des données
res = {}
deg = 1
# Boucle des simulations
for s in range(1, N+1):
	res[f'Simulation {s}'] = {a: {} for a in range(debut, fin+1)}
	sim = res[f'Simulation {s}']
	P = 0.1
	gard = False
	if SN == 3:
		while not gard:
			for annee in range(debut, fin+1):
				for i in range(9):
					germes[i] += 15
				alea = gen_alea(germes[0], germes[1], germes[2])
				alea_ntac = gen_alea(germes[3], germes[4], germes[5])
				alea_ntam = gen_alea(germes[6], germes[7], germes[8])
				if annee == 2018:
					sim[annee]['NTAC'] = 96133
					sim[annee]['NTAM'] = 3066
					sim[annee]['NTANM'] = 93067
					sim[annee]['NTT'] = 3485
					sim[annee]['NTB'] = 136974
					sim[annee]['NTBG'] = 8725
					sim[annee]['NTBL'] = 128249
					sim[annee]['NMTJ'] = 9.55
				else:
					NTAC = ntac(sim[annee-1]['NTAC'], alea, alea_ntac)
					sim[annee]['NTAC'] = NTAC
					NTAM = ntam(NTAC, sim[annee-1]['NTAC'], sim[annee-1]['NTAM'], alea, alea_ntam)
					sim[annee]['NTAM'] = abs(NTAM)
					NTANM = ntanm(NTAC, NTAM)
					sim[annee]['NTANM'] = NTANM
					NTT = ntt(NTAM, sim[annee-1]['NTT'], sim[annee-1]['NTAM'], alea)
					sim[annee]['NTT'] = abs(NTT)
					NTB = ntb(NTAC, sim[annee-1]['NTB'], sim[annee-1]['NTAC'], alea)
					sim[annee]['NTB'] = NTB
					NTBG = ntbg(NTB, alea)
					sim[annee]['NTBG'] = NTBG
					NTBL = ntbl(NTB, NTBG)
					sim[annee]['NTBL'] = NTBL
					NMTJ = nmtj(NTT)
					sim[annee]['NMTJ'] = NMTJ

				gard = True
				if annee >= 2026:
					if sim[annee]['NTT'] > 2000:
						gard = False
						P += 0.1
						break
	else:
		for annee in range(debut, fin+1):
			for i in range(9):
				germes[i] += 15
			alea = gen_alea(germes[0], germes[1], germes[2])
			alea_ntac = gen_alea(germes[3], germes[4], germes[5])
			alea_ntam = gen_alea(germes[6], germes[7], germes[8])
			if annee == 2018:
				sim[annee]['NTAC'] = 96133
				sim[annee]['NTAM'] = 3066
				sim[annee]['NTANM'] = 93067
				sim[annee]['NTT'] = 3485
				sim[annee]['NTB'] = 136974
				sim[annee]['NTBG'] = 8725
				sim[annee]['NTBL'] = 128249
				sim[annee]['NMTJ'] = 9.55
			else:
				NTAC = ntac(sim[annee-1]['NTAC'], alea, alea_ntac)
				sim[annee]['NTAC'] = NTAC
				NTAM = ntam(NTAC, sim[annee-1]['NTAC'], sim[annee-1]['NTAM'], alea, alea_ntam)
				sim[annee]['NTAM'] = NTAM
				NTANM = ntanm(NTAC, NTAM)
				sim[annee]['NTANM'] = NTANM
				NTT = ntt(NTAM, sim[annee-1]['NTT'], sim[annee-1]['NTAM'], alea)
				sim[annee]['NTT'] = NTT
				NTB = ntb(NTAC, sim[annee-1]['NTB'], sim[annee-1]['NTAC'], alea)
				sim[annee]['NTB'] = NTB
				NTBG = ntbg(NTB, alea)
				sim[annee]['NTBG'] = NTBG
				NTBL = ntbl(NTB, NTBG)
				sim[annee]['NTBL'] = NTBL
				NMTJ = nmtj(NTT)
				sim[annee]['NMTJ'] = NMTJ

	if P*10 > deg:
		deg = P*10

# Calcul des moyennes des indicateurs
res['Moyennes'] = {a: {} for a in range(debut, fin+1)}
moy = res['Moyennes']
for a in range(debut, fin+1):
	moy[a] = {i: 0 for i in ('NTAC', 'NTAM', 'NTANM', 'NTT', 'NTB', 'NTBG', 'NTBL', 'NMTJ')}
for a, b in res.items():
	if a != "Moyennes":
		for c, d in b.items():
			for e, f in d.items():
				moy[c][e] += f
for a, b in moy.items():
	for c, d in b.items():
		if c == "NMTJ":
			moy[a][c] = round(d / N, 2)
		else:
			moy[a][c] = d // N

#Calcul des intervalles de confiance à 95%
res['Intervalles de confiance'] = {a: {} for a in (2026, 2030)}
confiance = res['Intervalles de confiance']
for a in (2026, 2030):
	confiance[a] = {i: 0 for i in ('NTAC', 'NTAM', 'NTANM', 'NTT', 'NTB', 'NTBG', 'NTBL', 'NMTJ')}
for a, b in res.items():
	if a != "Moyennes" and a != "Intervalles de confiance":
		for c, d in b.items():
			if c == 2026 or c == 2030:
				for e, f in d.items():
					confiance[c][e] += (f - moy[c][e]) ** 2
for a, b in confiance.items():
	for c, d in b.items():
		x = moy[a][c] - 1.96 * (sqrt(d/N) / sqrt(N))
		y = moy[a][c] + 1.96 * (sqrt(d/N) / sqrt(N))
		if c == "NMTJ":
			x = round(x, 2)
			y = round(y, 2)
		else:
			x = int(x)
			y = int(y)
		confiance[a][c] = f"[{x}, {y}]"

op = 0
while op not in (1, 2, 3):
	print("\n→ Choisir une option:")
	print("1 : Afficher les résultats de la simulation sur la console")
	print("2 : Générer des fichiers Excel des résultats de la simulation")
	print("3 : Les deux")
	op = int(input())

def afficher():
	if N == 1:
		for a, b in res.items():
			if a != "Moyennes" and a != "Intervalles de confiance":
				print("\n" + "-" * (len(a)+4))
				print(f"| {a} |")
				print("-" * (len(a)+4))
				for c, d in b.items():
					print(f"• {c}")
					for e, f in d.items():
						if e == "NMTJ":
							print(f"{e} = {f}")
						else:
							print(f"{e} = {f}", end=", ")
	else:
		for a, b in res.items():
			print("\n" + "-" * (len(a)+4))
			print(f"| {a} |")
			print("-" * (len(a)+4))
			for c, d in b.items():
				print(f"• {c}")
				for e, f in d.items():
					if e == "NMTJ":
						print(f"{e} = {f}")
					else:
						print(f"{e} = {f}", end=", ")
	if SN == 3:
		print("\n ------------------")
		print(f"L'objectif a été atteint après la {int(deg)}ème réduction des bornes des intervalles par 10% ")

def gen_fichiers():
	for nom, donnees in res.items():
		d = donnees
		df = pd.DataFrame.from_dict(d, orient='index')
		df.to_excel(f'{nom}.xlsx')
	print("Les fichiers sont générés dans le même répertoire que le programme")

if op == 1:
	afficher()
elif op == 2:
	if pand:
		gen_fichiers()
	else:
		print("Pandas n'est pas installé")
else:
	if pand:
		gen_fichiers()
	else:
		print("Pandas n'est pas installé")
	afficher()
