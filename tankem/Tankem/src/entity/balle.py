## -*- coding: utf-8 -*-
from util import *

import sys
from direct.showbase.ShowBase import ShowBase
from panda3d.bullet import *
from panda3d.core import *
from panda3d.ai import *
from direct.interval.IntervalGlobal import *
import random

from direct.particles.ParticleEffect import ParticleEffect

class Balle(ShowBase):

    balleID = 0

    def __init__(self, identifiantLanceur,mondePhysique):
        self.mondePhysique = mondePhysique
        self.lanceurId = identifiantLanceur
        self.balleId = Balle.balleID
        Balle.balleID += 1

        self.forceApplique = Vec3(0,0,0)

        # On charge le modèles
        self.modele = loader.loadModel("../asset/Balle/ball")
        self.modele.reparentTo(render)
        #On réduit sa taille un peu...
        self.modele.setScale(0.5,0.5,0.5)

        #On ajoute une sphere de physique
        forme = BulletSphereShape(0.2)
        noeud = BulletRigidBodyNode("Balle")
        noeud.addShape(forme)
        self.noeudPhysique = render.attachNewNode(noeud)
        self.noeudPhysique.node().setMass(1.0)
        self.modele.reparentTo(self.noeudPhysique)

        self.accept("detonateur-explosion",self.detonateurDistance)

        self.noeudPhysique.setTag("EntiteTankem","Balle")
        self.noeudPhysique.setTag("balleId",str(self.balleId))
        self.noeudPhysique.setTag("lanceurId",str(self.lanceurId))

        self.pftExplosion = ParticleEffect()
        self.pftExplosion.loadConfig("../asset/Particle/tankemExplode.ptf")

        self.pftRacine = NodePath("Racine pfx expolision")
        self.pftRacine.reparentTo(render)

    def detonateurDistance(self, identifiantDetonateur):
        if(identifiantDetonateur == self.lanceurId):
            self.exploser()

    def exploser(self):
        if(self.etat == "actif"):
            self.etat = "explose"

            #Arrêt de la sequence de destruction automatique
            if hasattr(self, 'sequenceExplosionAutomatique'):
               self.sequenceExplosionAutomatique.finish()

            if hasattr(self, 'sequenceMissileGuide'):
               self.sequenceMissileGuide.finish()

            #On désactive le mouvement sur cette balle
            #Les collisions seront détectées mais la balle
            #ne bougera pas
            self.noeudPhysique.node().setKinematic(True)

            #self.modele.setTransparency(TransparencyAttrib.MAlpha)
            grosseurScaleFinal = 10.0
            self.modele.removeNode()

            intervalPhysique = LerpScaleInterval(self.noeudPhysique, 0.2, grosseurScaleFinal, 1.0)
            #intervalCouleur = LerpColorScaleInterval(self.modele,0.3,LVecBase4(0.8,0.2,0.2,0),self.modele.getColorScale())
            fonctionDetruire = Func(self.destroy)
            self.sequenceDetruire = Sequence(Wait(0.5),fonctionDetruire)

            intervalPhysique.start()
            self.sequenceDetruire.start()
            self.pftRacine.setPos(self.noeudPhysique.getPos())
            self.pftExplosion.start(parent = self.pftRacine, renderParent = self.pftRacine)

    def projetter(self, position, direction):
        self.etat = "actif"

        self.noeudPhysique.setPos(position)

        self.modele.setColorScale(0.8,0.3,0,1)
        
        self.noeudPhysique.node().setGravity(0.0)
        self.noeudPhysique.node().setLinearDamping(0.0)
        self.noeudPhysique.node().setFriction(0.0)
        self.noeudPhysique.node().setRestitution(2.0)
        vitesseBalle = 14
        self.noeudPhysique.node().applyCentralImpulse(direction * vitesseBalle)
        self.mondePhysique.attachRigidBody(self.noeudPhysique.node())

        self.intervalExplosion(1.2)

    def projetterRapide(self, position, direction):
        self.etat = "actif"

        self.noeudPhysique.setPos(position)

        self.modele.setColorScale(0.1,0.1,0,1)
        
        self.noeudPhysique.node().setGravity(0.0)
        self.noeudPhysique.node().setLinearDamping(0.0)
        self.noeudPhysique.node().setFriction(0.0)
        self.noeudPhysique.node().setRestitution(2.0)
        vitesseBalle = 18
        self.noeudPhysique.node().applyCentralImpulse(direction * vitesseBalle)
        self.mondePhysique.attachRigidBody(self.noeudPhysique.node())

        self.intervalExplosion(0.8)

    def projetterVariable(self, position, direction):
        self.etat = "actif"

        self.noeudPhysique.setPos(position)

        self.modele.setColorScale(0.9,0.9,0.9,1)
        
        self.noeudPhysique.node().setGravity(0.0)
        self.noeudPhysique.node().setLinearDamping(0.0)
        self.noeudPhysique.node().setFriction(0.0)
        self.noeudPhysique.node().setRestitution(2.0)
        vitesseBalle = 13
        self.noeudPhysique.node().applyCentralImpulse(direction * vitesseBalle)
        self.mondePhysique.attachRigidBody(self.noeudPhysique.node())

        self.intervalExplosion(0.5)

    def deposer(self, position, direction):
        self.etat = "actif"

        self.noeudPhysique.setPos(position)

        self.modele.setColorScale(0.3,0.9,0.3,1)
        
        self.noeudPhysique.node().setLinearDamping(0.7)
        self.noeudPhysique.node().setFriction(0.7)
        self.noeudPhysique.node().setRestitution(0.0)
        vitesseBalle = 4
        self.noeudPhysique.node().applyCentralImpulse(direction * vitesseBalle)
        self.mondePhysique.attachRigidBody(self.noeudPhysique.node())

        self.intervalExplosion(10)

    def appliquerForce(self):
        self.noeudPhysique.node().applyCentralForce(self.forceApplique)

    def lancer(self, position, direction, vitesseInitialeBalle=16):
        self.etat = "actif"

        self.modele.setColorScale(0.8,0.1,0.6,1)

        self.noeudPhysique.setPos(position)
        self.noeudPhysique.node().setMass(2.0)
        self.noeudPhysique.node().setLinearDamping(0.1)
        self.noeudPhysique.node().setAngularDamping(0.99)
        self.noeudPhysique.node().setFriction(0.9)
        self.noeudPhysique.node().setRestitution(1.0)

        self.accept("appliquerForce",self.appliquerForce)
        self.forceApplique = Vec3(0.0,0.0,-50)
        
        #On lancera à enciron 60 degré la balle
        directionFinale = direction + Vec3(0,0,3)
        directionFinale.normalize()
        self.noeudPhysique.node().setLinearVelocity(directionFinale * vitesseInitialeBalle)
        self.mondePhysique.attachRigidBody(self.noeudPhysique.node())

        self.intervalExplosion(3.0)

    def lancerGuide(self, position, noeudCible):
        #On ignore la direction du tank, on lance la balle dans les airs
        self.lancer(position, Vec3(0,0,1),vitesseInitialeBalle=18)

        #C'est un ange de la mort... on le colore rouge foncé!
        self.modele.setColorScale(0.3,0,0.1,1)

        #On créé ensuite une séquence pour le guidage automatique
        attendre = Wait(0.65)
        fonctionViser = Func(self.lancerSurCible, noeudCible)
        self.sequenceMissileGuide = Sequence(attendre,fonctionViser)
        self.sequenceMissileGuide.start()

    def lancerSurCible(self,noeudCible):
        #Calcul de la direction de la balle
        vecteurDifference = noeudCible.getPos() - self.noeudPhysique.getPos()
        vecteurDifference.normalize()
        vitesseInitialeBalle = 30
        self.noeudPhysique.node().setLinearVelocity(vecteurDifference * vitesseInitialeBalle)


    def intervalExplosion(self, delai):
        #On fait exploser la balle dans quelques secondes
        delai = Wait(delai)
        fonctionExploser = Func(self.exploser)
        self.sequenceExplosionAutomatique = Sequence(delai,fonctionExploser)
        self.sequenceExplosionAutomatique.start()

    def destroy(self):
        self.etat = "Detruit"
        self.pftExplosion.cleanup()
        self.mondePhysique.removeRigidBody(self.noeudPhysique.node())
        self.noeudPhysique.removeNode()

        #Enlève l'écoute des messages
        self.ignoreAll()