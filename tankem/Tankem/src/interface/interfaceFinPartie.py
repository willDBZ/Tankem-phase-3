# -*- coding: utf-8 -*-
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import *
from DTO_DAO import DAO_Oracle
from DTO_DAO import DTO
from direct.showbase.Transitions import Transitions
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import *
from direct.interval.LerpInterval import *
from direct.interval.IntervalGlobal import *
from direct.gui.OnscreenImage import OnscreenImage
import sys
from DTO_DAO.AnalyseDTOJoueur import AnalyseDTOJoueur
import random
import math

#pour afficher le tank
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletDebugNode
from entity import tank
from direct.actor.Actor import Actor



# auteur: William Tang
class InterfaceFinPartie():
    def __init__(self):
        # utilitaires
        self.lettres = []
        self.sequences = []
        
        self.ajouterTopFrame()

        #On dit à la caméra que le dernier modèle doit s'afficher toujours en arrière
        # self.baseSort = base.cam.node().getDisplayRegion(0).getSort()
        # base.cam.node().getDisplayRegion(0).setSort(20)
    
        


    def ajouterTopFrame(self):
        #le frame du top
        size = 0.75
        self.frameTop = DirectFrame(text="", frameColor=(25, 0.1, 0, 0.01), frameSize=(-size*2,size*2,-size,size), pos=(0,-1, 0))

        # ajouter un frame à gauche et un à droite pour chaque joueur
        for i in range(len(DTO.joueurs)):
            self.ajouterFrameJoueur(i, DTO.joueurs[i])


    def ajouterTexteGagnant(self, message):
        textSize = len(message)
        espace = 0.02
        if textSize >= 30:
            startScale = 0.14
            espace = 0.09
        elif textSize >= 20:
            startScale = 0.17
            espace = 0.12
        elif textSize >= 10:
            startScale = 0.20
            espace = 0.14
        else:
            startScale = 0.30
            espace = 0.19



        i = 0
        sequence = []
        for index,caractere in enumerate(message):
            
            label = OnscreenText(text = caractere, pos = (-1.5 + espace*index, -0.75), scale = startScale , align=TextNode.ACenter, mayChange = False)
            # #les deux intervals opposés (monter et descendre)
            duree = 0.5
            intervalUp = label.posInterval(duree, Point3(0,0,0.2), startPos=Point3(0,0,0), blendType = 'easeIn')
            intervalDown = label.posInterval(duree, Point3(0,0,0), startPos=Point3(0,0,0.2), blendType = 'easeOut')
            # # # la loop qui dure toujours
            #truc 1:
            # sequence = Sequence(intervalUp,intervalDown)
            # sequenceDepart = Sequence(Wait(0.3 * i), sequence)
            
            # sequenceDepart.loop()


            # truc 2:
            
            sequence.append(Sequence(intervalUp,intervalDown))
            # b = sequence[i]
            b = i/21.0*3.14
            sequenceDepart = Sequence(Wait(math.sin(i/float(len(message))*3.14)), Func(lambda i = i, s = sequence: s[i].loop()))

            # sequenceDepart = Sequence(Func(lambda s = sequence : s[i].loop()))
            
            sequenceDepart.start()


            # self.sequences.append(sequence)
            self.lettres.append(label)
            i = i + 1


    def ajouterFrameJoueur(self, ordre, joueur):
        size = 0.75
        gauche = 1
        if ordre == 0:
            gauche = -1
        elif ordre == 1:
            gauche = 1
        frameJoueur = DirectFrame(text="", frameSize=(-size,size,-size,size), pos=(0.75 * gauche,-1, 0))
        frameJoueur.reparentTo(self.frameTop)

        
        frameContenu = DirectFrame(text="", frameColor=(0, 25, 0, 0.1), frameSize=(-size*0.75,size*0.75,-size*0.90,size*0.90), pos=(0,-1,0))
        frameContenu.reparentTo(frameJoueur)

        # ajouter les labels pour les infos sur le joueur
        labelNom = OnscreenText(text = joueur.nom, pos = (0, 0.60), scale = 0.14, bg = (255,255,255,1))
        labelNom.reparentTo(frameContenu)

        messages = ["niveau: ","exp initial: ","exp gagné: ", "exp actuel: "]
        values = [joueur.level,joueur.ancienExperience,joueur.gainExperience,joueur.experience]
        for i in range(4):
            message = messages[i] + str(values[i])
            self.ajouterLabelInfo(frameContenu,message, i)
        # labelNom = OnscreenText(text = 'Niveau: ', pos = (0, 0.45), scale = 0.07, bg = (255,255,255,1))
        # labelNom.reparentTo(frameContenu)

        # ajouter la couronne pour le joueur gagnant
        if joueur.vainqueur:
            self.imageCouronne = OnscreenImage(parent = frameContenu , image = '../asset/Menu/couronne.png', pos = (-0.5, 0, 0.8), scale = (0.2,1,0.2),hpr = (0,0,-35))
            self.imageCouronne.setTransparency(TransparencyAttrib.MAlpha)
            self.ajouterTexteGagnant(joueur.message)

        # si le joueur a gagné de niveau
        if joueur.levelUp:
            imageLevelUp = OnscreenImage(parent = frameContenu , image = '../asset/Menu/levelUp.png', pos = (-0.6, 0, 0.1), scale = (0.2,1,0.2))
            imageLevelUp.setTransparency(TransparencyAttrib.MAlpha)

            # le label pour le level up
            labelLevelUp = OnscreenText(text = "Level Up!", pos = (-0.6, 0.4), scale = 0.11)
            labelLevelUp.reparentTo(frameContenu)
            labelLevelUp.hide()

            # interval
            duree = 2
            intervalUp = imageLevelUp.posInterval(duree, Point3(-0.6, 0, 0.3), startPos=Point3(-0.6, 0, 0.1), blendType = 'easeIn')
            sequence = Sequence(Func(lambda : imageLevelUp.show()),
                        intervalUp,
                        Func(lambda : imageLevelUp.hide()),
                        Func(lambda : labelLevelUp.show()),
                        Wait(1),
                        Func(lambda : labelLevelUp.hide()),
                        Wait(1)
                        )
            
            
            sequence.loop()




    def ajouterLabelInfo(self,parent,message,ordre):
        espace = 0.25
        label = OnscreenText(text = message, pos = (0, 0.45 - espace*ordre), scale = 0.11)

        label.reparentTo(parent)