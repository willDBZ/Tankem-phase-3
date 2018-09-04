## -*- coding: utf-8 -*-
#Ajout des chemins vers les librarires
from util import inclureCheminCegep
import sys

#Importe la configuration de notre jeu
from panda3d.core import loadPrcFile
loadPrcFile("config/ConfigTankem.prc")

#Module de Panda3DappendObject
from direct.showbase.ShowBase import ShowBase

#Modules internes
from gameLogic import GameLogic
from interface import InterfaceMenuPrincipal
from DTO_DAO import *
 
class Tankem(ShowBase):
    def __init__(self):  
        ShowBase.__init__(self)
        # mode Lazy: créer la connexion Oracle dès le début du programme
        dao = DAO_Oracle() # forcer la création du Singleton
        etatConnexion = dao.getConnexionState()
        if etatConnexion:
            dao.fillLookupTableArmes()
        self.demarrer()

    def demarrer(self):
        self.gameLogic = GameLogic(self)
        #Commenter/décommenter la ligne de votre choix pour démarrer le jeu
        #Démarre dans le menu
        # self.menuPrincipal = InterfaceMenuPrincipal()
        #Démarre directement dans le jeu
        # messenger.send("DemarrerPartie")
        #Démarrer directement le menu de cartes
        messenger.send("DemarrerMenuNiveau")
        #Démarre directement le menu de connexion
        # messenger.send("DemarrerConnexion")
        #Démarre directement la page de fin de partie
        # messenger.send("DemarrerPageFinPartie")
        

#Main de l'application.. assez simple!
app = Tankem()
app.run()
