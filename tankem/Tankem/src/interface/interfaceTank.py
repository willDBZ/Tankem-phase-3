## -*- coding: utf-8 -*-
from util import *

from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText 
from direct.gui.DirectGui import *
from panda3d.core import *
from direct.interval.LerpInterval import *
from direct.interval.IntervalGlobal import *
 
class InterfaceTank(ShowBase):
	def __init__(self, identificateurTank, couleurBarre):
		self.identificateurTank = identificateurTank

		#On doit créer une couleur avec 4 composantes sinon ça crash... beurk
		couleurBarreAlpha = Vec4(couleurBarre.getX(),couleurBarre.getY(),couleurBarre.getZ(),1)

		positionBarreVie = Vec3(-1.1,0,0.85) #tank 0
		if(identificateurTank == 1): #tank 1
			positionBarreVie.setX(1.1)

		self.barreVie = DirectWaitBar(barColor = couleurBarreAlpha, text = "", value = 100, pos = positionBarreVie, scale=0.5)

		couleurChargeAlpha = couleurBarreAlpha * 0.8
		positionBarreCharge = Vec3(-1.4,0,0.75) #tank 0
		if(identificateurTank == 1): #tank 1
			positionBarreCharge.setX(1.4)
		self.barCharge = DirectWaitBar(barColor = couleurChargeAlpha, text = "", value = 100, pos = positionBarreCharge, scale=0.2)

		self.accept("effetPointDeVie",self.effetPointDeVie)
		self.accept("effetRecharge",self.effetRecharge)

	def effetPointDeVie(self,identificateurTank,nouvelleValeur):
		if(self.identificateurTank == identificateurTank):
			self.changerValeurPointDeVie(nouvelleValeur)


	def effetRecharge(self,identificateurTank,duree):
		if(self.identificateurTank == identificateurTank):
			effetRecharge = LerpFunc(self.changerValeurCharge,fromData=0,toData=100, duration=duree, blendType='easeOut')
			effetRecharge.start()

	def changerValeurPointDeVie(self,nouvelleValeur):
			self.barreVie['value'] = nouvelleValeur

	def changerValeurCharge(self,nouvelleValeur):
			self.barCharge['value'] = nouvelleValeur