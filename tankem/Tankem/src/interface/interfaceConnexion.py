## -*- coding: utf-8 -*-
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import *
from DTO_DAO import DAO_Oracle
from DTO_DAO import DTO
from direct.showbase.Transitions import Transitions
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import *
from direct.interval.LerpInterval import *
from direct.interval.IntervalGlobal import *
import sys
from DTO_DAO.AnalyseDTOJoueur import AnalyseDTOJoueur
import random
import textwrap

#pour afficher le tank
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletDebugNode
from entity import tank
from direct.actor.Actor import Actor

# pour le sanitizer
from DTO_DAO.Sanitizer import Sanitizer

# auteur: William Tang
class InterfaceConnexion():
    def __init__(self):
        #utilitaires
        self.analyse = AnalyseDTOJoueur()
        self.labels = []
        self.drs = []
        self.sequences = []
        self.tankModels = []

        # champs de textes
        #le frame du haut
        self.ajouterTopFrame()

        # Background image
        # on a commenté le background, pcq ca cachait les scènes pour les deux chars
        # self.background = OnscreenImage(parent = render2d , image = '../asset/Menu/menuLogin.png', )
        
        #On dit à la caméra que le dernier modèle doit s'afficher toujours en arrière
        self.baseSort = base.cam.node().getDisplayRegion(0).getSort()
        base.cam.node().getDisplayRegion(0).setSort(20)

        self.controlTextScale = 0.10
        self.controlBorderWidth = (0.005,0.005)
    


        #Initialisation de l'effet de transition
        curtain = loader.loadTexture("../asset/Menu/loading.jpg")

        self.transition = Transitions(loader)
        self.transition.setFadeColor(0, 0, 0)
        self.transition.setFadeModel(curtain)

        self.sound = loader.loadSfx("../asset/Menu/demarrage.mp3")
       
        self.testerConnexion()


    def connexion(self, joueur):
        ordre = joueur + 1

        # vérifier si le joueur n'est pas déjà connecté
        if (joueur == 0 and DTO.joueur1 != None) or (joueur == 1 and DTO.joueur2 != None):
            self.labelMessage.setText("ATTENTION! Joueur %d est DÉJÀ connecté!"%(ordre))
            return

        if joueur == 0:
            user = self.entryUser1.get()
            pw = self.entryMDP1.get()
        else:
            user = self.entryUser2.get()
            pw = self.entryMDP2.get()

        # vérifier que le joueur ne se connecte pas deux fois
        if (DTO.joueur1 != None and DTO.joueur1.nom == user) or (DTO.joueur2 != None and DTO.joueur2.nom == user):
            self.labelMessage.setText("ATTENTION! L'usager %s est DÉJÀ connecté!"%(user))
            return


            
        # faire une connexion à la bd
        self.dao = DAO_Oracle()
        connecte = self.dao.validerUsager(user, pw, joueur)


        # ajuster le message de l'état de connexion des joueurs
        if connecte:          
            self.labelMessage.setText("Joueur %d est connecté!"%(ordre))
            if joueur == 0:
                self.ajouterChar(joueur,DTO.joueur1.couleur)
            elif joueur == 1:
                self.ajouterChar(joueur,DTO.joueur2.couleur)
            self.afficherMessagesSanitizer(joueur)

            if DTO.joueur1 != None and DTO.joueur2 != None:
                self.labelMessage.setText("Les deux joueurs sont connectés!")
                self.ajouterMiddleFrame()
                self.ajouterBottomFrame()
                if len(DTO.joueurs) == 0:
                    DTO.joueurs.append(DTO.joueur1)
                    DTO.joueurs.append(DTO.joueur2)
            indexJoueur = joueur
        else:
            self.labelMessage.setText("Erreur de login pour Joueur %d "%(ordre))

    def ajouterTopFrame(self):
        #le frame du top
        self.frameTop = DirectFrame(text="")
        self.frameTop.reparentTo(base.a2dTopLeft)

        #les 4 labels de joueurs et mot de passe
        labelJoueur1 = OnscreenText(text = 'Joueur 1', pos = (0.25, -0.10), scale = 0.07, bg = (255,255,255,1), frame = (0,0,0,1))
        labelMotDePasse1 = OnscreenText(text = 'Mot de passe 1', pos = (0.25, -0.30), scale = 0.07, bg = (255,255,255,1), frame = (0,0,0,1))
        labelJoueur2 = OnscreenText(text = 'Joueur 2', pos = (2.00, -0.10), scale = 0.07, bg = (255,255,255,1), frame = (0,0,0,1))
        labelMotDePasse2 = OnscreenText(text = 'Mot de passe 2', pos = (2.00, -0.30), scale = 0.07, bg = (255,255,255,1), frame = (0,0,0,1))

        labelJoueur1.reparentTo(self.frameTop)
        labelMotDePasse1.reparentTo(self.frameTop)
        labelJoueur2.reparentTo(self.frameTop)
        labelMotDePasse2.reparentTo(self.frameTop)

        #les quatre boîtes de saisie de texte
        #pour le joueur 1
        self.entryUser1 = DirectEntry(text = "", scale=.07, pos = (0.65, 0.0,-0.10), numLines = 1, focus=1)
        self.entryUser1.reparentTo(self.frameTop)

        self.entryMDP1 = DirectEntry(text = "", scale=.07, pos = (0.65, 0.0,-0.3),command = lambda x = 1: self.connexion(0), numLines = 1, focus=1, obscured = True)
        self.entryMDP1.reparentTo(self.frameTop)
        
        #pour le joueur 2
        self.entryUser2 = DirectEntry(text = "", scale=.07, pos = (2.4, 0.0,-0.10), numLines = 1, focus=1)
        self.entryUser2.reparentTo(self.frameTop)

        self.entryMDP2 = DirectEntry(text = "", scale=.07, pos = (2.4, 0.0,-0.3),command = lambda x = 1: self.connexion(1), numLines = 1, focus=1, obscured = True)
        self.entryMDP2.reparentTo(self.frameTop)

        self.frameConnecte = DirectFrame(text="")
        self.frameConnecte.reparentTo(self.frameTop)

        #label pour le message
        height = 0.10
        self.frameMessage = DirectFrame(text="", frameColor=(255,255,255,0.23), frameSize=(-1.2,1.2,-height,height))
        self.frameMessage.setPos(0,0,0.55)
        self.labelMessage = OnscreenText(text = 'Aucun message', pos = (0, 0), scale = 0.07, align=TextNode.ACenter, mayChange = True)
        self.labelMessage.reparentTo(self.frameMessage)
        
    def ajouterChar(self, ordre,couleur):
        # https://www.panda3d.org/manual/index.php/File:DisplayRegion_1.jpg
        if ordre == 0:
            dr2 = base.win.makeDisplayRegion(0, 0.30, 0, 0.5)
        elif ordre == 1:
            dr2 = base.win.makeDisplayRegion(0.70, 1, 0, 0.5)
        
        dr2.setClearColor(VBase4(0.41, 0.41, 0.41, 0))
        dr2.setClearColorActive(True)
        dr2.setClearDepthActive(True)

        render2 = NodePath('render')
        cam2 = render2.attachNewNode(Camera('cam2'))
        dr2.setCamera(cam2)

        cam2.setPos(-22.5, -387.3, 58.1999)
        
        env = loader.loadModel("box.egg")
        env.setTransparency(TransparencyAttrib.MAlpha)
        env.setDepthTest(False)
        env.setDepthWrite(False)
        env.reparentTo(render2)

        # ajouter le tank
        size = 50
        tank = Actor("../asset/Tank/tank")
        tank.setScale(size,size,size)
        tank.setColorScale(couleur[0], couleur[1],couleur[2],1)
        if ordre == 0:
            tank.setHpr(270.0, 0.0, 0.0)
        elif ordre == 1:
            tank.setHpr(90.0, 0.0, 0.0)
        tank.reparentTo(env)
        
        #faire avancer le tank
        if ordre == 0:
            intervalAvancer = tank.posInterval(2, Point3(-10, 4, 8), startPos=Point3(-200, 4, 8))
        elif ordre == 1:
            intervalAvancer = tank.posInterval(2, Point3(-10, 4, 8), startPos=Point3(180, 4, 8))


        # faire tourner le tank (interval)
        duree = 3.0
        if ordre == 0:
            intervalTourner = tank.hprInterval(duree, Vec3(-90, 0, 0))
        else:
            intervalTourner = tank.hprInterval(duree, Vec3(450, 0, 0))

        sequenceAvancer = Sequence(intervalAvancer)
        sequenceTourner = Sequence(intervalTourner)


        sequence = Sequence(sequenceAvancer,
            Func(sequenceTourner.loop)
        )
        sequence.start()

        self.drs.append(dr2)
        self.sequences.append(sequenceTourner)
        self.tankModels.append([ordre,tank])
        
        
    def ajouterMiddleFrame(self):
        height = 0.15
        self.frameMiddle = DirectFrame(frameColor=(255,255,255,0.23), frameSize=(-1.2,1.2,-height,height))
        self.frameMiddle.setPos(0,0,0.25)
        
        #calculer les noms des deux joueurs
        
        joueur1 = self.analyse.calculerNom(DTO.joueur1)
        joueur2 = self.analyse.calculerNom(DTO.joueur2)
        

        dist = 0.075
        labelVS1 = OnscreenText(text = joueur1, pos = (0, 0.05), scale = 0.07, align=TextNode.ACenter, mayChange = True)
        labelVS1.reparentTo(self.frameMiddle)
        labelVS = OnscreenText(text = 'VS', pos = (0, 0.05 - dist), scale = 0.07, align=TextNode.ACenter, mayChange = True)
        labelVS.reparentTo(self.frameMiddle)
        labelVS2 = OnscreenText(text = joueur2, pos = (0, 0.05 - dist*2), scale = 0.07 , align=TextNode.ACenter, mayChange = True)
        labelVS2.reparentTo(self.frameMiddle)

       
    def combattre(self):

        
        # freezer le bouton Combattre
        scaleBouton = self.b.getScale().getX()
        coordonnees = []
        tankH1 = self.tankModels[0][1].getH()
        tankH2 = self.tankModels[1][1].getH()
        coordonnees.append(tankH1)
        coordonnees.append(tankH2)


        for sequence in self.sequences:
            sequence.finish()

        cpt = 0
        sequenceTourner = None 

        dureeTourner = 3.0
        for listTank in self.tankModels:
            
            ordre = listTank[0]
            tank = listTank[1]

            tank.setH(coordonnees[cpt])

            
            if ordre == 0:
                intervalTourner = tank.hprInterval(dureeTourner, Vec3(-90, 0, 0))
            elif ordre == 1:
                intervalTourner = tank.hprInterval(dureeTourner, Vec3(450, 0, 0))

            sequenceTourner = Sequence(intervalTourner)
            sequenceTourner.start()
            cpt = cpt + 1


        self.b.setScale(scaleBouton)


        sequence = Sequence(
            Func(lambda: sequenceTourner.start()),
            Wait(dureeTourner),
            Func(lambda : self.ajouterTextVS()),
            Wait(5.5),
            Func(lambda: self.chargerJeu())
            )
        sequence.start()
    

    def analyserPositionChars(self):
        arrete = False
        arrete = self.tankModels[0][1].getH() == -90 and self.tankModels[1][1].getH() == 450
        return arrete
            




    def ajouterTextVS(self):
        message = DTO.joueur1.nom + " VS " + DTO.joueur2.nom
        self.labelVS = OnscreenText(text = message, shadow = (0,0,0,1),pos = (0, 0),frame = (0,0,0,1), scale = 0.14 , align=TextNode.ACenter, mayChange = False, bg = (0,255,0,0.5), fg = (255,255,255,1))

        #faire l'animation du texte
        scaleDebut = 1.0
        scaleFin = 2.0
        duree = 2.0

        # #les deux intervals opposés (grandir vs rapetir)
        intervalRapetir = self.labelVS.scaleInterval(duree, Vec3(scaleDebut,scaleDebut,scaleDebut))
        intervalGrossir = self.labelVS.scaleInterval(duree, Vec3(scaleFin,scaleFin,scaleFin))

        # # # la loop qui dure toujours
        sequence = Sequence(intervalGrossir,intervalRapetir)
        sequence.loop()

    def afficherMessagesSanitizer(self,joueur):
        if joueur == 0:
            messagesErreurs = DTO.messagesErreurs1
        elif joueur == 1:
            messagesErreurs = DTO.messagesErreurs2
        for i in range(len(messagesErreurs)):
            height = 0.15
            width = 0.4
            textSize = 0.05

            if joueur == 0:
                positionArrivee = Point3(-1.1,0,-0.1)
                positionDepart = Point3(-2.5,0,-0.1)
            elif joueur == 1:
                positionArrivee = Point3(1.1,0,-0.1)
                positionDepart = Point3(2.5,0,-0.1)

            
            message = messagesErreurs[i].retournerMessage()
            message = textwrap.fill(message, 33)
            self.frameErreur = DirectFrame(text=message, pos = positionDepart, frameColor=(255,255,255,0.5), frameSize=(-width,width,-height,height))
            self.frameErreur["text_scale"] = (textSize,textSize)
            self.frameErreur["text_fg"] = (255,0,0,1)
            self.frameErreur["text_pos"] = (0,0.1)
            
            scaleFin = 0
            intervalEntrer = self.frameErreur.posInterval(2, positionArrivee, startPos=positionDepart)
            intervalRapetisser = self.frameErreur.scaleInterval(1, Vec3(1,1,scaleFin))
            
            tempsAttente = i * 8
            sequence = Sequence(
                Wait(tempsAttente),
                intervalEntrer, 
                Wait(5),
                intervalRapetisser
            )
            sequence.start()




    def ajouterBottomFrame(self):
        #variables de positionnement
        height = 0.15
        width = 0.6
        dist = 0.1
        debut = 0.025

        #frame combattre
        self.frameBottom = DirectFrame(text="", frameColor=(255,255,255,0.23), frameSize=(-width,width,-height,height))
        self.frameBottom.setPos(0,0,-0.10)
        labelCombattre = OnscreenText(text = 'Combattrons dans', pos = (0, debut), scale = 0.07 , align=TextNode.ACenter, mayChange = True)
        labelCombattre.reparentTo(self.frameBottom)
        nomNiveau = DTO.nomMap
        if nomNiveau == None:
            nomNiveau = ""
        labelNiveau = OnscreenText(text = nomNiveau, pos = (0, debut-dist), scale = 0.07 , align=TextNode.ACenter, mayChange = True)
        # labelNiveau = OnscreenText(text = DTO.mapSelectionne.titre, pos = (0, debut-dist), scale = 0.07 , align=TextNode.ACenter, mayChange = True)
        labelNiveau.reparentTo(self.frameBottom)

        height = 0.10
        width = 0.6
        dist = 0.1
        debut = -0.025
        #frame joueur favorisé
        #déterminer le joueur favorisé
        if DTO.joueurs[0].level > DTO.joueurs[1].level:
            joueurFavorise = DTO.joueurs[0].nom
            DTO.joueurs[0].favori
        elif DTO.joueurs[1].level > DTO.joueurs[0].level:
            joueurFavorise = DTO.joueurs[1].nom
            DTO.joueurs[1].favori = True
        else:
            joueurFavorise = None

        if joueurFavorise == None:
            joueurFavorise = "Aucun joueur favorisé!"
        else:
            # joueurFavorise = self.analyse.calculerNom(DTO.joueurs[0])
            joueurFavorise += " est favorisé!"

        self.frameFavori= DirectFrame(text="", frameColor=(24,24,0,1), frameSize=(-width,width,-height,height))
        self.frameFavori.setPos(0,0,-0.40)
        labelFavori= OnscreenText(text = joueurFavorise, pos = (0, debut), scale = 0.06 , align=TextNode.ACenter, mayChange = True)
        labelFavori.reparentTo(self.frameFavori)

        # bouton combattre
        self.b = DirectButton(text = ("COMBATTRE!"), scale=.07,frameSize = (-6,6,-3,3),pos=(0,0,-0.65) ,command=self.combattre)
        self.b.reparentTo(self.frameBottom)

        # interval de "battements de coeur" pour le bouton Combattre
        # les paramètres de la séquence
        scaleDebut = 0.03
        scaleFin = 0.05
        self.b.setScale(scaleDebut,scaleDebut,scaleDebut)
        duree = 0.75

        #les deux intervals opposés (grandir vs rapetir)
        intervalGrossir = self.b.scaleInterval(duree, Vec3(scaleDebut,scaleDebut,scaleDebut))
        intervalRapetir = self.b.scaleInterval(duree, Vec3(scaleFin,scaleFin,scaleFin))

        # la loop qui dure toujours
        sequence = Sequence(intervalRapetir ,intervalGrossir)
        sequence.loop()
        self.sequences.append(sequence)

    def chargerJeu(self): 
            #loader les données dans le DTO avec la bonne map
            self.dao = DAO_Oracle()
            self.dao.fillGame(DTO.idMap)

            #On démarre!
            Sequence(Func(lambda : self.transition.irisOut(0.2)),
                     SoundInterval(self.sound),
                     Func(self.cacher),
                     Func(lambda : messenger.send("DemarrerPartie")),
                     Wait(0.2), #Bug étrange quand on met pas ça. L'effet de transition doit lagger
                     Func(lambda : self.transition.irisIn(0.2))
            ).start()

    def cacher(self):
            #Est esssentiellement un code de "loading"
            #On remet la caméra comme avant
            base.cam.node().getDisplayRegion(0).setSort(self.baseSort)
            # #On cache les menus
            # self.background.hide()
            self.frameTop.hide()
            self.frameBottom.hide()
            self.frameMiddle.hide()
            self.frameMessage.hide()
            self.frameFavori.hide()
            self.labelVS.hide()
            for dr in self.drs:
                base.win.removeDisplayRegion(dr)
       

    def testerConnexion(self):
        dao = DAO_Oracle()
        connecte = dao.connectDB()
        if not connecte:
            self.labelMessage.setText("Aucune connexion avec la base de données...")