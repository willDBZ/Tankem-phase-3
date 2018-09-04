# -*- coding: utf-8 -*-
 # auteur: William Tang
from DTO_DAO.Joueur import Joueur
class DTO():
	maps = []
	cases = []
	problemeOracle = True
	# joueurs = [Joueur(self,x,y,ordre,nom, couleur, password, experience, vie, force, agilite,dexterite, id, message)]
	# joueurs = [Joueur(0,0,1,"superman",(0,0,0), "AAAaaa111", 0, 0, 99999,5,9999999,1, "Joueur 1 gagne"), Joueur(0,0,0,"megaman",(255,255,255), "AAAaaa111", 0, 0, 0,5,5, 2, "Joueur 2 gagne")]
	# joueur1 = Joueur(0,0,1,"superman",[333,0,0], "AAAaaa111", 0, 1, 1,1,1,1, "Joueur 1ff")
	# joueur2 = Joueur(0,0,1,"superman",[0,0,0], "AAAaaa111", 9999, 1, 1,1,1,1, "Joueur 1ff")
	joueur1 = None
	joueur2 = None
	joueurs = []
	id_gagnant = None
	mapSelectionne = None
	idMap = None
	nomMap = None

	#pour le temps de début et de fin
	finPartie = None
	debutPartie = None

	# pour le sanitizer
	messagesErreurs1 = None
	messagesErreurs2 = None

	etatConnexionOracle = False
	
	def __init__(self):
		pass

	

	