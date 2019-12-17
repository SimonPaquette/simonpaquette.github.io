"""
Les Matrices
	forme echelonee
	forme echelonne reduite
	solution du systeme (matrice augmentee)
	inverse
	determinant
"""

import numpy as np
from random import randrange
from math import gcd
from fractions import Fraction
from pandas import DataFrame


def valeurMatrice ():
	"""
	None -> Mat2D
	Demander les valeurs de la matrice
	"""
	matrice=[]

	while True:
		ligne=input()
		if not ligne: 
			break
		valeurs=ligne.split()
		rangee=[int(val) for val in valeurs]
		matrice.append(rangee)

	return matrice

def creerVotreMatrice (carree=False):
	"""
	Bool -> Mat2D
	Creer votre propre matrice (condition possible)
	"""
	print()
	print("Entrez les nombres avec des espaces entre les colonnes.")
	print("Une rangee par ligne, et une ligne vide a la fin.")
	matrice=valeurMatrice()

	while True:

		#si matrice vide
		if matrice==[]:
			print("Veuillez entrer un matrice...")
			matrice=valeurMatrice()
			continue

		#si matrice non valide
		liste_colonne_par_ligne=[]
		for ligne in matrice:
			liste_colonne_par_ligne.append(len(ligne))

		colonne_egal=True
		for index in range(len(liste_colonne_par_ligne)-1):
			if liste_colonne_par_ligne[index]!=liste_colonne_par_ligne[index+1]:
				colonne_egal=False

		if not colonne_egal:
			print("Veuillez entrer un matrice valide...")
			matrice=valeurMatrice()
			continue

		#condition matrice carree
		total_ligne, total_colonne=tailleMatrice(matrice)
		if carree and total_ligne!=total_colonne:
			print("Veuillez entrer une matrice carree...")
			matrice=valeurMatrice()
			continue
			
		#matrice valide
		matrice=np.reshape(matrice,(total_ligne,total_colonne))
		return matrice	

def tailleMatrice (matrice):
	"""
	Mat2D -> (int,int)	
	Obtenir la taille de la matrice MxN
	"""
	total_ligne=len(matrice)
	total_colonne=len(matrice[0])

	return (total_ligne,total_colonne)

def formatage (taille, parametres=None):
	"""
	(int,int), str  -> [list,list]
	Avoir les parametres formant la matrice
	TYPE : 
		"LX" -> Equation (L) + Variable (X)
		"LXB" -> Equation (L) + Variable (X) + Solution (B)
	"""
	index,columns=[],[]

	if parametres=="LX":
		for value in range(1,taille[0]+1):
			index.append("L"+str(value))
		for value in range(1,taille[1]+1):
			columns.append("x"+str(value))

	elif parametres=="LXB":
		for value in range(1,taille[0]+1):
			index.append("L"+str(value))
		for value in range(1,taille[1]):
			columns.append("x"+str(value))
		columns.append("b")	

	elif parametres!=None:
		print("ERREUR : parametres formatage()")

	return [index,columns]

def printMatrice (matrice, variable):
	"""
	Mat2D, [list,list] -> None
	Imprimer la matrice ordonnee
	"""
	print(DataFrame(matrice,index=variable[0],columns=variable[1]))

def convertFloat (matrice):
	"""
	Mat2D (int) -> Mat2D (float)
	Convertir la matrice pour avoir des decimales
	"""
	matrice=matrice.astype(float)

	return matrice

def ME (matrice):
	"""
	Mat2D -> Mat2D
	Echelonner la matrice
	"""
	total_ligne,total_colonne=tailleMatrice(matrice)
	#pour debuter a [0][0], se deplacant vers le bas de gauche a droite
	m=0		#m ligne
	n=0		#n colonne
	while(m<total_ligne and n<total_colonne):

		#changement de ligne si l'element pivot est egal a 0
		if matrice[m][n]==0:
			error=True

			#recherche d'une nouvelle ligne contenant un pivot a cette colonne
			for ligne in range(m+1,total_ligne):
				if matrice[ligne][n]!=0:
					numero_ligne=ligne
					error=False
					break

			#si presence de colonnes nulles, deplacement des colonnes pivots vers la droite 
			if error==True:
				n+=1
				continue

			#inversion des lignes trouvees
			ligne_depart=np.copy(matrice[numero_ligne])
			ligne_remplace=np.copy(matrice[m])

			matrice[m]=ligne_depart
			matrice[numero_ligne]=ligne_remplace
	
		#etablissement du point et de la ligne de reference
		pivot=matrice[m][n]									#point de pivot
		ligne_base=matrice[m]								#ligne du pivot

		#creation de 0 en-dessous des points de pivots
		for ligne in range(m+1,total_ligne):

			ligne_calcul=matrice[ligne]						#ligne a changer
			valeur_init=matrice[ligne][n]					#valeur situe a la meme colonne que le pivot

			#reduction par denominateur commun
			deno_commun=gcd(int(pivot),int(valeur_init))	
			if deno_commun==0:
				deno_commun=1
			
			#calcul
			for colonne in range(n,total_colonne):
				ligne_calcul[colonne]=((ligne_calcul[colonne]*pivot)-(ligne_base[colonne]*valeur_init))/deno_commun
		
		#travail sur le pivot suivant
		m+=1
		n+=1


	total_ligne, total_colonne=tailleMatrice(matrice)
	matrice=np.reshape(matrice,(total_ligne,total_colonne))
	return matrice

def MR (matrice):
	"""
	Mat2D -> Mat2D
	Reduire la matrice
	"""
	total_ligne,total_colonne=tailleMatrice(matrice)
	#pour debuter a la derniere ligne, se deplacant vers le haut de gauche a droite
	m=total_ligne-1		#m ligne				
	while m>=0:

		#si ligne nulle a la fin, passe a la ligne au-dessus
		ligne_nulle=True
		for colonne in range(total_colonne):
			if matrice[m][colonne]!=0:
				ligne_nulle=False
				#Pour trouver la colonne pivots
				colonne_pivot=colonne
				break
		if ligne_nulle==True:
			m-=1
			continue

		#etablissement du point et de la ligne de reference
		pivot=matrice[m][colonne_pivot]						#point de pivot
		ligne_base=matrice[m]								#ligne du pivot
	
		#creation de 0 au-dessus des points de pivots
		for ligne in range(m-1,-1,-1):

			ligne_calcul=matrice[ligne]						#ligne a changer
			valeur_init=matrice[ligne][colonne_pivot]		#valeur situe a la meme colonne que le pivot

			#reduction par denominateur commun
			deno_commun=gcd(int(pivot),int(valeur_init))	
			if deno_commun==0:
				deno_commun=1

			#calcul
			for colonne in range(total_colonne):
				ligne_calcul[colonne]=((ligne_calcul[colonne]*pivot)-(ligne_base[colonne]*valeur_init))/deno_commun

		#travail sur la ligne plus haute
		m-=1	

	return matrice

def MER (matrice):
	"""
	Mat2D -> Mat2D
	Avoir la matrice echelonee reduite
	"""
	total_ligne,total_colonne=tailleMatrice(matrice)
	for ligne in range(total_ligne):
		valeur_pivot=1		#au cas quil y a une ligne sans pivot

		#trouver le pivot dans chaque ligne
		for colonne in range(total_colonne):
			if matrice[ligne][colonne]!=0:
				valeur_pivot=matrice[ligne][colonne]
				break

		#diviser toutes les valeurs de la ligne par celle du pivot
		for colonne in range(total_colonne):
			matrice[ligne][colonne]/=valeur_pivot
			if matrice[ligne][colonne]==-0.:
				matrice[ligne][colonne]=0

	return matrice

def valeurFraction (matrice):
	"""
	Mat2D -> Mat2D
	Convertir les valeurs float en fractions
	"""
	total_ligne,total_colonne=tailleMatrice(matrice)
	mat=[]
	for ligne in range(total_ligne):
		mat_ligne=[]
		for colonne in range(total_colonne):
			valeur=matrice[ligne][colonne]
			valeur=str(Fraction(valeur).limit_denominator())
			mat_ligne.append(valeur)
		mat.append(mat_ligne)
		
	return mat

def solutionSysteme (matrice):
	"""
	Mat2D -> None
	Donner la solution du systeme matriciel
	"""
	total_ligne,total_colonne=tailleMatrice(matrice)
	total_pivot=0
	for ligne in range(total_ligne):
		for colonne in range(total_colonne):
			if matrice[ligne][colonne]!="0":
				total_pivot+=1
				if colonne==total_colonne-1:
					print("\nLe systeme est incompatible, aucune solution possible")
					total_pivot=None
				break
	if total_pivot!=None:
		if total_pivot==total_colonne-1:
			print("\nLe systeme est compatible, la solution est unique")
		elif total_pivot<total_colonne-1:
			print("\nLe systeme est compatible, avec une infinite de solutions")

def matriceIdentite (n):
	"""
	int -> Mat2D
	Creer In
	"""
	In=[]
	for ligne in range(n):
		In.append([])
		for colonne in range(n):
			if ligne==colonne:
				In[ligne].append(1)
			if ligne!=colonne:
				In[ligne].append(0)

	return(In)

def inverseExiste (matrice):
	"""
	Mat2D -> bool
	Verifie si la matrice inverse existe
	"""
	total_ligne,total_colonne=tailleMatrice(matrice)
	matrice=convertFloat(matrice)
	matrice=ME(matrice)
	matrice=MR(matrice)
	matrice=MER(matrice)

	In=matriceIdentite(total_ligne)

	inverse_existe=True
	for ligne in range(total_ligne):
		for colonne in range(total_colonne):
			if matrice[ligne][colonne]!=In[ligne][colonne]:
				inverse_existe=False

	return inverse_existe

def inverseAssemblage (matrice):
	"""
	Mat2D -> Mat2D
	Calcul la matrice inverse a l'aide de la matrice identite
	"""
	total_ligne,total_colonne=tailleMatrice(matrice)
	In=matriceIdentite(total_ligne)
	inverse_assemblage=[]
	for ligne in range(total_ligne):
		inverse_assemblage.append([])
		for colonne in range(total_colonne*2):
			if colonne<total_colonne:
				inverse_assemblage[ligne].append(matrice[ligne][colonne])
			else:
				inverse_assemblage[ligne].append(In[ligne][colonne-total_colonne])
	
	total_ligne, total_colonne=tailleMatrice(inverse_assemblage)
	inverse_assemblage=np.reshape(inverse_assemblage,(total_ligne,total_colonne))

	return inverse_assemblage

def inverseResultat (matrice_et_In):
	"""
	Mat2D -> Mat2D
	Return la matrice inverse finale
	"""
	total_ligne,total_colonne=tailleMatrice(matrice_et_In)
	inverse=[]
	for ligne in range(total_ligne):
		inverse.append([])
		for colonne in range(total_colonne//2):
			inverse[ligne].append(matrice_et_In[ligne][colonne+total_colonne//2])

	total_ligne, total_colonne=tailleMatrice(inverse)
	inverse=np.reshape(inverse,(total_ligne,total_colonne))
	
	return inverse

def calculDeterminant (matrice, taille):
	"""
	Mat2D -> int
	Calcul le determinant de la matrice
	"""
	if taille==2:
		det=matrice[0][0]*matrice[1][1]-matrice[1][0]*matrice[0][1]
		return det

	else:
		#creer les sous-matrice
		mat_dict={}
		for pos in range(taille):
			mat_dict["mat"+str(pos)]=[]
			for ligne in range(1,taille):
				mat_dict["mat"+str(pos)].append([])
				for colonne in range(taille):
					if colonne!=pos:
						mat_dict["mat"+str(pos)][ligne-1].append(matrice[ligne][colonne])

		#calcul de chacun des determinants
		det=0
		for pos in range(taille):
			mat=mat_dict.get("mat"+str(pos))
			det+=((-1)**(pos+2))*matrice[0][pos]*calculDeterminant(mat,taille-1)
	
	return det
	
	
"""
pour plus tard -> 
	changer solution systeme pour donner le vecteur de la solution (unique et infinite)
	valeurs et vecteurs propres
	multiplication de matrice
"""
##########################
if __name__ == "__main__":

	choix=input("Que voulez-vous calculer comme matrice?\n"+
				"\tLa forme echelonee, (e)\n"+
				"\tLa forme echelonne reduite, (r)\n"+
				"\tLa solution du systeme matriciel - matrice augmentee, (s)\n"+
				"\tLa matrice inverse, (i)\n"+
				"\tLe determinant de la matrice, (d)\n"+
				"Votre choix : ")

	while True:
		if (choix!="e" and choix!="r" and choix!="s" and choix!="i" and choix!="d"):
			choix=input("Faites un choix valide : ")
		else:
			break

	if choix=="e":
		matrice=creerVotreMatrice()
		nombre_ligne,nombre_colonne=tailleMatrice(matrice)
		variable=formatage((nombre_ligne,nombre_colonne),"LX")
		print("Soit la matrice de depart :\n")
		printMatrice(matrice,variable)
		matrice=convertFloat(matrice)
		matrice=ME(matrice)
		matrice=valeurFraction(matrice)
		print("\nVoici sa forme echelonne :\n")
		printMatrice(matrice,variable)

	if choix=="r":
		matrice=creerVotreMatrice()
		nombre_ligne,nombre_colonne=tailleMatrice(matrice)
		variable=formatage((nombre_ligne,nombre_colonne),"LX")
		print("Soit la matrice de depart :\n")
		printMatrice(matrice,variable)
		matrice=convertFloat(matrice)
		matrice=ME(matrice)
		matrice=MR(matrice)
		matrice=MER(matrice)
		matrice=valeurFraction(matrice)
		print("\nVoici sa forme echelonne reduite :\n")
		printMatrice(matrice,variable)

	if choix=="s":
		matrice=creerVotreMatrice()
		nombre_ligne,nombre_colonne=tailleMatrice(matrice)
		variable=formatage((nombre_ligne,nombre_colonne),"LXB")
		print("Soit la matrice de depart :\n")
		printMatrice(matrice,variable)
		matrice=convertFloat(matrice)
		matrice=ME(matrice)
		matrice=MR(matrice)
		matrice=MER(matrice)
		matrice=valeurFraction(matrice)
		print("\nVoici sa forme echelonne reduite :\n")
		printMatrice(matrice,variable)
		solutionSysteme(matrice)

	if choix=="i":
		matrice=creerVotreMatrice(True)
		nombre_ligne,nombre_colonne=tailleMatrice(matrice)
		variable=formatage((nombre_ligne,nombre_colonne),"LX")
		print("Soit la matrice de depart :\n")
		printMatrice(matrice,variable)
		if inverseExiste(matrice):
			matrice=inverseAssemblage(matrice)
			matrice=convertFloat(matrice)
			matrice=ME(matrice)
			matrice=MR(matrice)
			matrice=MER(matrice)
			matrice=valeurFraction(matrice)
			matrice=inverseResultat(matrice)
			print("\nVoici la matrice inverse :\n")
			printMatrice(matrice,variable)			
		else:
			print("\nCette matrice na pas de matrice inverse")

	if choix=="d":
		matrice=creerVotreMatrice(True)
		nombre_ligne,nombre_colonne=tailleMatrice(matrice)
		variable=formatage((nombre_ligne,nombre_colonne),"LX")
		print("Soit la matrice :\n")
		printMatrice(matrice,variable)
		determinant=calculDeterminant(matrice,nombre_ligne)
		print("\nLe determinant de la matrice est :",determinant)