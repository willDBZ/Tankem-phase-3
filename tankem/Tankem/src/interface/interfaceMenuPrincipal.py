## -*- coding: utf-8 -*-

from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText 
from direct.gui.DirectGui import *
from panda3d.core import *
from direct.interval.LerpInterval import *
from direct.interval.IntervalGlobal import *
from direct.showbase.Transitions import Transitions
import sys

class InterfaceMenuPrincipal(ShowBase):
    def __init__(self):

        #Image d'arrière plan
        self.background=OnscreenImage(parent=render2d, image="../asset/Menu/menuPrincipal.jpg")

        #On dit à la caméra que le dernier modèle doit s'afficher toujours en arrière
        self.baseSort = base.cam.node().getDisplayRegion(0).getSort()
        base.cam.node().getDisplayRegion(0).setSort(20)

        #Titre du jeu
        self.textTitre = OnscreenText(text = "Tankem!",
                                      pos = (0,0.6), 
                                      scale = 0.32,
                                      fg=(0.8,0.9,0.7,1),
                                      align=TextNode.ACenter)

        #Boutons
        btnScale = (0.18,0.18)
        text_scale = 0.12
        borderW = (0.04, 0.04)
        couleurBack = (0.243,0.325,0.121,1)
        separation = 0.5
        hauteur = -0.6
        self.b1 = DirectButton(text = ("Jouer", "!", "!", "disabled"),
                          text_scale=btnScale,
                          borderWidth = borderW,
                          text_bg=couleurBack,
                          frameColor=couleurBack,
                          relief=2,
                          command=self.chargeJeu,
                          pos = (-separation,0,hauteur))


        self.b2 = DirectButton(text = ("Quitter", "Bye!", ":-(", "disabled"),
                          text_scale=btnScale,
                          borderWidth = borderW,
                          text_bg=couleurBack,
                          frameColor=couleurBack,
                          relief=2,
                          command = lambda : sys.exit(),
                          pos = (separation,0,hauteur))
        #Initialisation de l'effet de transition
        curtain = loader.loadTexture("../asset/Menu/loading.jpg")

        self.transition = Transitions(loader)
        self.transition.setFadeColor(0, 0, 0)
        self.transition.setFadeModel(curtain)

        self.sound = loader.loadSfx("../asset/Menu/demarrage.mp3")

    def cacher(self):
            #Est esssentiellement un code de "loading"

            #On remet la caméra comme avant
            base.cam.node().getDisplayRegion(0).setSort(self.baseSort)
            #On cache les menus
            self.background.hide()
            self.b1.hide()
            self.b2.hide()
            self.textTitre.hide()

    def chargeJeu(self):
            #On démarre!
            Sequence(Func(lambda : self.transition.irisOut(0.2)),
                     SoundInterval(self.sound),
                     Func(self.cacher),
                     Func(lambda : messenger.send("DemarrerMenuNiveau")),
                     Wait(0.2), #Bug étrange quand on met pas ça. L'effet de transition doit lagger
                     Func(lambda : self.transition.irisIn(0.2))
            ).start()
