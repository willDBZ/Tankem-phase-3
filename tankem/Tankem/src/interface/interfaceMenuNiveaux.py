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
import textwrap



class InterfaceMenuNiveaux(ShowBase):
    def __init__(self):
        self.frames = []
        self.dao = DAO_Oracle()
        # remplir les maps seulement si la connexion Oracle est fonctionnelle
        if self.dao.getConnexionState():
            self.dao.fill_dto_with_db()
        else:
            self.afficherMessagesOracle()

        # Background image
        self.background = OnscreenImage(parent = render2d , image = '../asset/Menu/tank.jpg')
        
        #On dit à la caméra que le dernier modèle doit s'afficher toujours en arrière
        self.baseSort = base.cam.node().getDisplayRegion(0).getSort()
        base.cam.node().getDisplayRegion(0).setSort(20)

        mapInfo = []
        for i in range(len(DTO.maps)):
            mapInfo.append((DTO.maps[i].titre,DTO.maps[i].id))
            


        self.controlTextScale = 0.10
        self.controlBorderWidth = (0.005,0.005)
        self.scrollItemButtons = self.createAllItems(mapInfo)

        

        verticalOffsetControlButton = 0.225
        verticalOffsetCenterControlButton = -0.02
        self.myScrolledListLabel = DirectScrolledList(

                # bouton Haut et ses parametres
                decButton_pos = (0.0,0.0, verticalOffsetControlButton + verticalOffsetCenterControlButton),
                decButton_text = "Haut",
                decButton_text_scale = 0.08,
                decButton_borderWidth = (0.0025,0.0025),
                decButton_frameSize = (-0.35, 0.35, -0.0375, 0.075),
                decButton_text_fg = (0.15, 0.15, 0.75, 1.0),
                # decButton_clickSound = ("../asset/Menu/btn-Son.mp3"),
                    

                 # bouton bas et ses parametres
                incButton_pos = (0.0, 0.0, -0.625 - verticalOffsetControlButton + verticalOffsetCenterControlButton),
                
                incButton_text = "Bas",
                incButton_text_scale = 0.08,
                incButton_borderWidth = (0.0025, 0.0025),
                incButton_frameSize = (-0.35, 0.35, -0.0375, 0.075),
                incButton_text_fg = (0.15, 0.15, 0.75, 1.0),
                # incButton_clickSound = ("../asset/Menu/btn-Son.mp3"),
                pos = (0, 0, 0.5),

                items = self.scrollItemButtons,

                # nombre de map visible par 'Scroll' ici c'est 3
                numItemsVisible = 5,
                forceHeight = 0.175,
                
                frameSize = (-1.05, 1.05, -0.95, 0.325),
                frameColor = (0.5, 0.5, 0.5, 0.75),

                itemFrame_pos = (0.0, 0.0, 0.0),
                itemFrame_frameSize = (-1.025, 1.025, -0.775, 0.15),
                itemFrame_frameColor = (0.35, 0.35, 0.35, 0.75),
                itemFrame_relief = 1,
            )

        self.quitterButton = DirectButton(

                # les 4 parametres indiques les differents types d'état que le bouton px avoir
                 #( lorsque tu survole lorsque tu clique etc)
                 text = ("Quitter", "Etes-Vous Sur?","Au Revoir!!","disabled"),
                 text_scale = self.controlTextScale,
                 borderWidth = self.controlBorderWidth,
                 relief = 2,
                 pos = (0.0,0.0, -0.75),
                 frameSize = (-0.5,0.5,-0.625, 0.105),
                 command = lambda : sys.exit(),
             )

        #Initialisation de l'effet de transition
        curtain = loader.loadTexture("../asset/Menu/loading.jpg")

        self.transition = Transitions(loader)
        self.transition.setFadeColor(0, 0, 0)
        self.transition.setFadeModel(curtain)

        self.sound = loader.loadSfx("../asset/Menu/demarrage.mp3")

    # creation du bouton avec le nom de la map
    def createItemButton (self,nomMap,idMap):
        return DirectButton(
            text = nomMap,
            text_scale = self.controlTextScale,
            borderWidth = self.controlBorderWidth,
            relief = 2,
            frameSize = (-1.0,1.0,-0.0625,0.105),
            command = lambda: self.chargerJeu(idMap,nomMap)
        )

    #Creation de la Map Aleatoire
    def createAllItems(self,mapsInfo):
        scrollItemButtons = [self.createItemButton(u'*-> Map au Hasard <-*',None)]
        for mapInfo in mapsInfo:
            pass
            scrollItemButtons.append(self.createItemButton(self.formatText(mapInfo[0]),mapInfo[1]))
        return scrollItemButtons

    # format du texte a mettre dans le bouton

    def formatText(self,text,maxLength = 30):
        return text if len(text) <= maxLength else text[0:maxLength] + '...'


    def chargerJeu(self,idMap, nomMap): 
            #loader les données dans le DTO avec la bonne map
            DTO.idMap = idMap
            # pour éviter de refaire une requête juste pour connaître le nom de la map
            DTO.nomMap = nomMap

            #On démarre!
            if self.dao.getConnexionState():
                transition = "DemarrerConnexion"
            else:
                transition = "DemarrerConnexion"

            Sequence(Func(lambda : self.transition.irisOut(0.2)),
                     SoundInterval(self.sound),
                     Func(self.cacher),
                     Func(lambda : messenger.send(transition)),
                     Wait(0.2), #Bug étrange quand on met pas ça. L'effet de transition doit lagger
                     Func(lambda : self.transition.irisIn(0.2))
            ).start()

    def afficherMessagesOracle(self):
        height = 0.15
        width = 0.30
        textSize = 0.05
        message = "Attention! La connexion au serveur Oracle n'est pas établie! Les choix de niveaux n'ont pas pu être chargés!"
        message = textwrap.fill(message, 25)
        positionDepart =  Point3(-1.37,0,1.5)
        positionArrivee =  Point3(-1.37,0,0.3)
        frameErreur = DirectFrame(text=message, pos = positionDepart, frameColor=(255,255,255,1), frameSize=(-width,width,-height,height))
        frameErreur["text_scale"] = (textSize,textSize)
        frameErreur["text_fg"] = (255,0,0,1)
        frameErreur["text_pos"] = (0,0.1)

        intervalEntrer = frameErreur.posInterval(1.5, positionArrivee, startPos=positionDepart)

        sequence = Sequence(
            intervalEntrer
        )
        sequence.start()

        self.frames.append(frameErreur)

    def cacher(self):
            #Est esssentiellement un code de "loading"
            #On remet la caméra comme avant
            base.cam.node().getDisplayRegion(0).setSort(self.baseSort)
            #On cache les menus
            self.background.hide()
            
            for item in self.scrollItemButtons:
                item.hide()
            self.quitterButton.hide()
            self.myScrolledListLabel.hide()    

            for item in self.frames:
                item.hide()      
