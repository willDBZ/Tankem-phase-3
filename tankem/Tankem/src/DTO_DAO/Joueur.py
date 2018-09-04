# -*- coding: utf-8 -*-
import math
 # auteur: William Tang
class Joueur():
	def __init__(self,x,y,ordre,nom, couleur, password, experience, vie, force, agilite,dexterite, id, message):
		self.x = x
		self.y = y
		self.ordre = ordre
		self.nom = nom
		self.couleur = couleur
		self.password = password
		self.experience = experience
		self.ancienExperience = None
		self.gainExperience = None
		self.distance = 0
		self.attributs = {"vie":vie, "force":force,"agilite":agilite,"dexterite":dexterite}
		self.vainqueur = False
		self.favori = False
		self.level = self.calculerLevel()
		self.tank = None
		self.id = id
		self.ajusterCouleur()
		self.message = message
		self.levelUp = False

	def ajusterCouleur(self):
		# diviser chaque valeur rgb dans couleur par 255
		listTempo = list(self.couleur)
		for i in range(len(self.couleur)):
			listTempo[i] = float(self.couleur[i]) / float(255)
		self.couleur = list(listTempo)
			

	def getAttribut(self,attribut):
		for i in range(len(self.attributs)):
			if attribut == self.attributs[i][0]:
				return self.attributs[i][1]

		return None

	def updateExperience(self,tank, tankEnemi):
		ancienLevel = self.level
		nouveauExp = 0
		self.ancienExperience = self.experience
		if self.vainqueur:
			nouveauExp = nouveauExp + 100
			if not self.favori:
				nouveauExp = nouveauExp + 100
			nouveauExp = nouveauExp + 2 * tank.pointDeVie
			self.experience = self.experience + nouveauExp
		else:
			viePerdueGagnant = tankEnemi.pointDeVieMax - tankEnemi.pointDeVie
			nouveauExp = 2 * viePerdueGagnant
			
			self.experience = self.experience + nouveauExp

		
		self.gainExperience = nouveauExp
		# déterminer si le joueur a gagné un niveau
		self.calculerLevel()
		if self.level > ancienLevel:
			self.levelUp = True
		else:
			self.levelUp = False
		return self.levelUp

	def calculerLevel(self):
		self.level = 0
        #formule pour calculer l'experience
		if self.experience < 100:
			self.level = 0
		else:
			self.level = math.sqrt((self.experience/50)-1)
			# l'arrondir vers le haut
			self.level = math.floor(self.level)
		return self.level