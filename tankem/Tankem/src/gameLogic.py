# -*- coding: utf-8 -*-
from util import *

from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletDebugNode
import datetime

#Modules de notre jeu
from map import Map
from inputManager import InputManager
from interface import *

#les interfaces graphiques
from interface import InterfaceMenuNiveaux
from interface import InterfaceFinPartie

#base de données
from DTO_DAO import DAO_Oracle
from DTO_DAO import DTO

#Classe qui gère les phases du jeu (Menu, début, pause, fin de partie)
class GameLogic(ShowBase):
    def __init__(self,pandaBase):
        self.pandaBase = pandaBase
        self.pandaBase.enableParticles()
        self.accept("DemarrerPartie",self.startGame)
        self.accept("DemarrerMenuNiveau",self.startMenu)
        self.accept("DemarrerConnexion",self.startConnexion)
        self.accept("tankElimine",self.gameOver)
        self.accept("DemarrerPageFinPartie",self.pageFinPartie)

    def pageFinPartie(self):
        self.dao = DAO_Oracle()
        # on affiche les résultats de fin de partie seulement si la connexion oracle fonctionne
        if self.dao.getConnexionState():
            self.pageFinPartie = InterfaceFinPartie()
        

    def gameOver(self,idPerdant):
        # si la connexion oracle fonctionone, on insère les données dans la bd
        dao = DAO_Oracle()
        if dao.getConnexionState():
            #mettre l'état du joueur gagnant à Vrai
            if idPerdant == 0:
                indexGagnant = 1 # joueur 2 a gagné
            elif idPerdant == 1:
                indexGagnant = 0 # joueur 1 a gagné
            DTO.joueurs[indexGagnant].vainqueur = True

            # ajuster les niveaux des deux joueurs
            analyse = AnalyseDTOJoueur()
            # for i in range(2):
            tanks = self.map.listTank

            #ajouter les expériences pour joueur 1 
            levelUp1 = DTO.joueurs[0].updateExperience(tanks[0],tanks[1])
            
            #ajouter les expériences pour joueur 2
            ancienLevel = DTO.joueurs[1].calculerLevel()
            DTO.joueurs[1].updateExperience(tanks[1],tanks[0])
            nouveauLevel = DTO.joueurs[1].calculerLevel()
            if (nouveauLevel > ancienLevel):
                levelUp = True

            #ajouter les statistiques d'armes au DTO
            for i in range(len(self.map.listTank)):
                DTO.joueurs[i].tank = self.map.listTank[i]

            # ajouter la date de fin de partie
            now = datetime.datetime.now()
            DTO.finPartie = datetime.datetime.now()

            self.dao = DAO_Oracle()
            self.dao.envoyerStatistiques()
            
            # après que tous les nouvelles statistiques sont calculées et/ou envoyées
            # on affiche les résultats de la partie
            messenger.send("DemarrerPageFinPartie")
        # sinon, on ne fait qu'afficher le nom du joueur gagnant
        else:
            pass

    def setup(self):
        self.setupBulletPhysics()

        self.setupCamera()
        self.setupMap()
        self.setupLightAndShadow()

        #Création d'une carte de base
        #self.carte.creerCarteParDefaut()
        if DTO.mapSelectionne == None:
            self.map.construireMapHasard()
        else:
            self.map.construireMapChoisi()

        # le temps de début de partie
        now = datetime.datetime.now()
        DTO.debutPartie = now

        #A besoin des éléments de la map
        self.setupControle()
        self.setupInterface()

        #Fonction d'optimisation
        #DOIVENT ÊTRE APPELÉE APRÈS LA CRÉATION DE LA CARTE
        #Ça va prendre les modèles qui ne bougent pas et en faire un seul gros
        #en faisant un seul gros noeud avec
        self.map.figeObjetImmobile()

        #DEBUG: Décommenter pour affiche la hiérarchie
        #self.pandaBase.startDirect()

        messenger.send("ChargementTermine")

    def startGame(self):
        # self.menu.run()
        self.setup()
        #On démarrer l'effet du compte à rebour.
        #La fonction callBackDebutPartie sera appelée à la fin
        self.interfaceMessage.effectCountDownStart(3,self.callBackDebutPartie)
        self.interfaceMessage.effectMessageGeneral("Appuyer sur F1 pour l'aide",3)

    def startMenu(self):
        self.menu = InterfaceMenuNiveaux()

    def startConnexion(self):
        self.menuConnexion = InterfaceConnexion()

    def setupBulletPhysics(self):
        debugNode = BulletDebugNode('Debug')
        debugNode.showWireframe(True)
        debugNode.showConstraints(True)
        debugNode.showBoundingBoxes(False)
        debugNode.showNormals(False)
        self.debugNP = render.attachNewNode(debugNode)

        self.mondePhysique = BulletWorld()
        self.mondePhysique.setGravity(Vec3(0, 0, -9.81))
        self.mondePhysique.setDebugNode(self.debugNP.node())
        taskMgr.add(self.updatePhysics, "updatePhysics")

        taskMgr.add(self.updateCarte, "updateCarte")

    def setupCamera(self):
        #On doit désactiver le contrôle par défaut de la caméra autrement on ne peut pas la positionner et l'orienter
        self.pandaBase.disableMouse()

        #Le flag pour savoir si la souris est activée ou non n'est pas accessible
        #Petit fail de Panda3D
        taskMgr.add(self.updateCamera, "updateCamera")
        self.setupTransformCamera()


    def setupTransformCamera(self):
        #Défini la position et l'orientation de la caméra
        self.positionBaseCamera = Vec3(0,-18,32)
        camera.setPos(self.positionBaseCamera)
        #On dit à la caméra de regarder l'origine (point 0,0,0)
        camera.lookAt(render)

    def setupMap(self):
        self.map = Map(self.mondePhysique)
        #On construire la carte comme une coquille, de l'extérieur à l'intérieur
        #Décor et ciel
        self.map.construireDecor(camera)
        #Plancher de la carte
        self.map.construirePlancher()
        #Murs et éléments de la map

    def setupLightAndShadow(self):
        #Lumière du skybox
        plight = PointLight('Lumiere ponctuelle')
        plight.setColor(VBase4(1,1,1,1))
        plnp = render.attachNewNode(plight)
        plnp.setPos(0,0,0)
        camera.setLight(plnp)

        #Simule le soleil avec un angle
        dlight = DirectionalLight('Lumiere Directionnelle')
        dlight.setColor(VBase4(0.8, 0.8, 0.6, 1))
        dlight.get_lens().set_fov(75)
        dlight.get_lens().set_near_far(0.1, 60)
        dlight.get_lens().set_film_size(30,30)
        dlnp = render.attachNewNode(dlight)
        dlnp.setPos(Vec3(-2,-2,7))
        dlnp.lookAt(render)
        render.setLight(dlnp)

        #Lumière ambiante
        alight = AmbientLight('Lumiere ambiante')
        alight.setColor(VBase4(0.25, 0.25, 0.25, 1))
        alnp  = render.attachNewNode(alight)
        render.setLight(alnp)

        #Ne pas modifier la valeur 1024 sous peine d'avoir un jeu laid ou qui lag
        dlight.setShadowCaster(True, 1024,1024)
        #On doit activer l'ombre sur les modèles
        render.setShaderAuto()

    def setupControle(self,):
        #Créer le contrôle
        #A besoin de la liste de tank pour relayer correctement le contrôle
        self.inputManager = InputManager(self.map.listTank,self.debugNP,self.pandaBase)
        self.accept("initCam",self.setupTransformCamera)

    def setupInterface(self):
        self.interfaceTank = []
        self.interfaceTank.append(InterfaceTank(0,self.map.listTank[0].couleur))
        self.interfaceTank.append(InterfaceTank(1,self.map.listTank[1].couleur))

        self.interfaceMessage = InterfaceMessage()

    def callBackDebutPartie(self):
        #Quand le message d'introduction est terminé, on permet aux tanks de bouger
        self.inputManager.debuterControle()

    #Mise à jour du moteur de physique
    def updateCamera(self,task):
        #On ne touche pas à la caméra si on est en mode debug
        if(self.inputManager.mouseEnabled):
            return task.cont

        vecTotal = Vec3(0,0,0)
        distanceRatio = 1.0
        if (len(self.map.listTank) != 0):
            for tank in self.map.listTank:
                vecTotal += tank.noeudPhysique.getPos()
            vecTotal = vecTotal/len(self.map.listTank)

        vecTotal.setZ(0)
        camera.setPos(vecTotal + self.positionBaseCamera)
        return task.cont

    #Mise à jour du moteur de physique
    def updatePhysics(self,task):
        dt = globalClock.getDt()
        messenger.send("appliquerForce")
        self.mondePhysique.doPhysics(dt)

        #Analyse de toutes les collisions
        for entrelacement in self.mondePhysique.getManifolds():
            node0 = entrelacement.getNode0()
            node1 = entrelacement.getNode1()
            
            self.map.traiterCollision(node0, node1)
        return task.cont

    def updateCarte(self,task):
        self.map.update(task.time)
        return task.cont
