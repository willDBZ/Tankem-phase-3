# -*- coding: utf-8 -*-
from util import *

import sys
from direct.showbase.ShowBase import ShowBase
from panda3d.bullet import *
from panda3d.core import *
from panda3d.ai import *
from direct.interval.IntervalGlobal import *
import random

class Arbre(ShowBase):
    def __init__(self,mondePhysique, treeGenerator):
        # On charge le modèles
        self.modele = treeGenerator.addTree(8,3)
        self.mondePhysique = mondePhysique
        formeCollision = BulletCapsuleShape(0.3 , 4)
        noeud = BulletRigidBodyNode('Arbre')
        decalagePosition = TransformState.makePos(Vec3(0,0,2))
        noeud.addShape(formeCollision,decalagePosition)
        self.noeudPhysique = render.attachNewNode(noeud)
        self.modele.reparentTo(self.noeudPhysique)
        self.noeudPhysique.node().setFriction(0.5)
        self.noeudPhysique.node().setRestitution(0.5)
        self.mondePhysique.attachRigidBody(noeud)

        #L'arbre ne bougera pas, on met donc le flag d'animation à True
        noeud.setKinematic(True)

        self.noeudPhysique.reparentTo(render)