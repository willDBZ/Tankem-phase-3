# -*- coding: utf-8 -*-
from util import *

import sys
from direct.showbase.ShowBase import ShowBase
from panda3d.bullet import *
from panda3d.core import *
from panda3d.ai import *
from direct.interval.IntervalGlobal import *


class Item(ShowBase):
    #Variable statique afin d'avoir un identifiant unique par item
    #tout en les comptants
    compteItem = 0

    #on créé les items en 2 étapes afin de contourner 
    def __init__(self):
        #On ajoute une sphere de physique
        forme = BulletSphereShape(0.9)
        self.noeudCorpsRigide = BulletRigidBodyNode("Item")
        self.noeudCorpsRigide.addShape(forme)
        self.noeudCorpsRigide.setGravity(0)

        self.noeudPhysique = render.attachNewNode(self.noeudCorpsRigide)

    def initialisationComplete(self, armeId, mondePhysique, cleanUpFunc):
            self.mondePhysique = mondePhysique
            self.armeId = armeId
            self.etat = "actif"
            self.cleanUpFunction = cleanUpFunc

            #Attribut un identifiant unique et augmente le compte
            #Manière simple d'avoir un ID unique et de trouver l'objet dans l'index
            self.itemId = Item.compteItem
            Item.compteItem += 1

            # On charge le modèles
            self.modele = loader.loadModel("../asset/Arme/item")
            self.modele.reparentTo(render)

            #On ajuste la texture (l'image sur le modèle 3D) selon l'arme
            nomTexture = "../asset/Arme/Mitraillette.png"
            if(self.armeId == "Shotgun"):
                nomTexture = "../asset/Arme/Shotgun.png"
            if(self.armeId == "Grenade"):
                nomTexture = "../asset/Arme/Grenade.png"
            elif(self.armeId == "Piege"):
                nomTexture = "../asset/Arme/Piege.png"
            elif(self.armeId == "Guide"):
                nomTexture = "../asset/Arme/Homing.png"
            elif(self.armeId == "Spring"):
                nomTexture = "../asset/Arme/Spring.png"
            elif(self.armeId == "Mitraillette"):
                pass #Déjà défini par défaut

            image = loader.loadTexture(nomTexture)
            #Étrange, on doit passer 1 à setTexture pour que ça fonctionne...
            self.modele.setTexture(image,1)

            self.modele.reparentTo(self.noeudPhysique)
            self.mondePhysique.attachRigidBody(self.noeudCorpsRigide)

            self.noeudPhysique.setTag("EntiteTankem","Item")
            self.noeudPhysique.setTag("armeId",self.armeId)
            self.noeudPhysique.setTag("itemId",str(self.itemId))

            #Animation du blc
            #On va lui faire faire une rotation et un petite mouvement de haut en bas
            positionActuelle = self.modele.getPos()
            blocPosInterval1 = LerpPosInterval( self.modele,
                                                0.5,
                                                positionActuelle + Vec3(0,0,0.5),
                                                startPos=positionActuelle)
            blocPosInterval2 = LerpPosInterval( self.modele,
                                                0.5,
                                                positionActuelle,
                                                positionActuelle + Vec3(0,0,0.5))
            # Create and play the sequence that coordinates the intervals.
            self.mouvementItem = Sequence( blocPosInterval1,
                                      blocPosInterval2)
            self.mouvementItem.loop()

            #Rotation du block
            self.rotationItem = LerpHprInterval( self.modele,
                                            3,
                                            Point3(360, 0, 0),
                                            startHpr=Point3(0, 0, 0))
            self.rotationItem.loop()

            #Durée de vie du bloc
            #Il va disparaître après un certain temps
            delai = Wait(15)
            fonctionDetruire = Func(self.destroy)
            self.sequenceDetruireDelai = Sequence(delai,fonctionDetruire)
            self.sequenceDetruireDelai.start()

    def recupere(self):
        if(self.etat == "actif"):
            self.etat = "recupere"

            #Arrêt de la sequence de destruction automatique
            if hasattr(self, 'sequenceDetruireDelai'):
               self.sequenceDetruireDelai.pause()

            if(self.noeudPhysique.node() is not None):
                self.mondePhysique.removeRigidBody(self.noeudPhysique.node())
            #Effet de récupération
            self.modele.setTransparency(TransparencyAttrib.MAlpha)
            intervalCouleur = LerpColorScaleInterval(self.modele,0.3,LVecBase4(1,1,1,0),self.modele.getColorScale())
            self.intervalGrossissement = LerpScaleInterval(self.noeudPhysique, 0.2, 1.4, 1.0)
            fonctionDetruire = Func(self.destroy)
            self.sequenceDetruire = Sequence(intervalCouleur,fonctionDetruire)
            self.intervalGrossissement.start()
            self.sequenceDetruire.start()     

    def destroy(self):
        if(self.etat == "detruit"):
            return
        self.etat = "detruit"

        #Arret des séquences
        if hasattr(self, 'intervalGrossissement'):
            self.intervalGrossissement.finish()

        if hasattr(self, 'mouvementItem'):
            self.mouvementItem.finish()

        if hasattr(self, 'rotationItem'):
            self.rotationItem.finish()

        self.cleanUpFunction()
        #Ce code (ou celui dans recuperer) genere un warning dans bullet :-(

        if(self.noeudPhysique.node() is not None):
            self.mondePhysique.removeRigidBody(self.noeudPhysique.node())
            self.noeudPhysique.removeNode()
        if(self.modele.node() is not None):
            self.modele.removeNode()
