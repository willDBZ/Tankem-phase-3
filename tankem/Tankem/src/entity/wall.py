# -*- coding: utf-8 -*-
from util import *

import sys
from direct.showbase.ShowBase import ShowBase
from panda3d.bullet import *
from panda3d.core import *
from panda3d.ai import *
from direct.interval.IntervalGlobal import *
import random

class Wall(ShowBase):
    def __init__(self,mondePhysique):
        # On charge le modèles
        self.modele = loader.loadModel("../asset/Wall/Wall")
        self.mondePhysique = mondePhysique
        #On fait les cubes à peine plus petits afin que rien ne collisionne
        #Les groupes de collision ne fonctionnent pas alors on fait son possible... 
        HACK_VALUE = 0.98
        formeCollision = BulletBoxShape(Vec3(HACK_VALUE, HACK_VALUE, HACK_VALUE))
        noeud = BulletRigidBodyNode('Mur')
        decalagePosition = TransformState.makePos(Vec3(0,0,1))
        noeud.addShape(formeCollision,decalagePosition)
        self.noeudPhysique = render.attachNewNode(noeud)
        self.modele.reparentTo(self.noeudPhysique)
        self.noeudPhysique.node().setFriction(0.5)
        self.noeudPhysique.node().setRestitution(0.5)
        self.mondePhysique.attachRigidBody(noeud)

        #Empêche de pouvoir le bouger en le poussant
        noeud.setKinematic(True)

        self.noeudPhysique.reparentTo(render)

    def animate(self,noeudAnimation):
        #On parente le noeud d'animation et ça va fonctionner
        self.noeudPhysique.reparentTo(noeudAnimation)