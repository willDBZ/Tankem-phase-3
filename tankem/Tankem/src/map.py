## -*- coding: utf-8 -*-
from util import *
from entity import *

from direct.showbase import DirectObject
from panda3d.core import *
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import YUp
from direct.interval.IntervalGlobal import *
import random
from DTO_DAO import DTO
from DTO_DAO import DAO_Oracle
import datetime


#Module qui sert à la création des maps
class Map(DirectObject.DirectObject):
    def __init__(self, mondePhysique):
        #On garde le monde physique en référence
        self.mondePhysique = mondePhysique

        #initialisation des constantes utiles
        if DTO.mapSelectionne == None:
            self.map_nb_tuile_x = 10
            self.map_nb_tuile_y = 10
        else:
            self.map_nb_tuile_x = DTO.mapSelectionne.colonnes
            self.map_nb_tuile_y = DTO.mapSelectionne.rangees
        self.map_grosseur_carre = 2.0 #dimension d'un carré
        self.map_petite_valeur_carre = 0.05 #Afin de contourner des problèmes d'affichage, on va parfois décaler les carrés/animations d'une petite valeur. Par exmeple, on ne veut pas que les cubes animés passent dans le plancher.

        #On veut que le monde soit centré. On calcul donc le décalage nécessaire des tuiles
        self.position_depart_x = - self.map_grosseur_carre * self.map_nb_tuile_x / 2.0
        self.position_depart_y = - self.map_grosseur_carre * self.map_nb_tuile_y / 2.0

        #On déclare des listes pour les tanks, les items et les balles
        self.listTank = []
        self.listeItem = []
        self.listeBalle = []

        #Dictionnaire qui contient des noeuds animés.
        #On pourra attacher les objets de notre choix à animer
        self.dictNoeudAnimation = {}
        self.creerNoeudAnimationImmobile() #Pour être consistant, on créé une animation... qui ne bouge pas
        self.creerNoeudAnimationVerticale() #Animation des blocs qui bougent verticalement
        self.creerNoeudAnimationVerticaleInverse() #Idem, mais décalé

        #Création de l'objet qui génèrera des arbres pour nous
        self.treeOMatic  = treeMaker.TreeOMatic()

        #Initialise le contenu vide la carte
        #On y mettra les id selon ce qu'on met
        self.endroitDisponible = [[True for x in range(self.map_nb_tuile_y)] for x in range(self.map_nb_tuile_x)]

        #Message qui permettent la création d'objets pendant la partie
        self.accept("tirerCanon",self.tirerCanon)
        self.accept("tirerMitraillette",self.tirerMitraillette)
        self.accept("lancerGrenade",self.lancerGrenade)
        self.accept("lancerGuide",self.lancerGuide)
        self.accept("deposerPiege",self.deposerPiege)
        self.accept("tirerShotgun",self.tirerShotgun)

    def libererEndroitGrille(self,i,j,doitBloquer):
        self.endroitDisponible[i][j] = doitBloquer

    def figeObjetImmobile(self):
        self.noeudOptimisation.flattenStrong()



    #Construction de la Map aléatoire
    def construireMapHasard(self):

    #Interprétation du résultat de l'algo
        #Utilisation du module de création au hasard
        #Le module a un x et y inversé!
        maze = mazeUtil.MazeBuilder(self.map_nb_tuile_y, self.map_nb_tuile_x)
        maze.build()
        mazeArray = maze.refine(.6)
        for row in mazeArray:
            for cell in row:
                if(cell.type == 1):
                    typeMur = random.randint(0, 100)
                    #On créé des éléments!
                    #40% du temps un mur immobile (5% de chance d'avoir un arbre)
                    #5% du temps un arbre seul
                    #18% du temps un mur mobile (5% de chance d'avoir un arbre)
                    #17% du temps un mur mobile inverse (5% de chance d'avoir un arbre)
                    if(typeMur <= 40):
                        noeudAnimationDuMur = "AnimationMurVerticale" if typeMur <= 20 else "AnimationMurVerticaleInverse"
                        noeudAAttacher = None if random.randint(0, 20) != 0 else Arbre(self.mondePhysique,self.treeOMatic)
                        self.creerMur(cell.row, cell.col, noeudAnimationDuMur, noeudAAttacher)
                    elif(typeMur <= 45):
                        self.creerArbre(cell.row, cell.col)
                    else:
                        noeudAAttacher = None if random.randint(0, 20) != 0 else Arbre(self.mondePhysique,self.treeOMatic)
                        self.creerMur(cell.row, cell.col,"AnimationMurImmobile",noeudAAttacher)

        #Dans la carte par défaut, des items vont appraître constamment entre 3 et 7 secondes d'interval
        self.genererItemParInterval(3,7)

        # si on ne se connecte pas à oracle, on prends les valeurs par défaut
        dao = DAO_Oracle()
        if dao.getConnexionState() == False or DTO.idMap == -1:
            self.creerChar(6,6,0,Vec3(0.1,0.1,0.1),None) #Char noir
            self.creerChar(3,3,1,Vec3(0.6,0.6,0.5),None) #Char gris-jaune        
        else:
        # sinon on prend les couleurs du joueur
            joueur = DTO.joueurs[0]
            couleur = joueur.couleur
            self.creerChar(6,6,0,Vec3(couleur[0],couleur[1],couleur[2]),DTO.joueurs[0].attributs) #Char noir
            joueur = DTO.joueurs[1]
            couleur = joueur.couleur
            self.creerChar(3,3,1,Vec3(couleur[0],couleur[1],couleur[2]),DTO.joueurs[1].attributs) #Char gris-jaune   
        
    def construireMapChoisi(self):   
        # Si tu choisis une map dans la liste, alors construction de celle-ci
        for i in range(len(DTO.cases)):
            
            case = DTO.cases[i]
            noeudAAttacher = None
            arbrePlancher = False
            
            #Si la case est un arbre
            if case.arbre:

                # si l'arbre est sur un plancher fixe
                if case.type == 1:
                    self.creerArbre(case.colonne, case.rangee)
                    arbrePlancher = True

                # si sur un mur animer, attacher l'arbre a celui-ci
            else:
                            
                noeudAAttacher = Arbre(self.mondePhysique,self.treeOMatic)
            
            # Si pas d'arbre ET que la tuile n'est pas un p^lancher
            if arbrePlancher == False and case.type != 1:
                if case.type == 2:
                    noeudAnimationDuMur = "AnimationMurVerticale"
                elif case.type == 3:
                    noeudAnimationDuMur = "AnimationMurVerticaleInverse"
                elif case.type == 4:
                    noeudAnimationDuMur = "AnimationMurImmobile"
                self.creerMur(case.colonne, case.rangee, noeudAnimationDuMur, noeudAAttacher)
           

        # Creation des joueurs et positionnement de ceux-ci sur la map
        for i in range(2):
            joueur = DTO.joueurs[i]
            x = joueur.x
            y = joueur.y
            if i == 0:
                couleur = joueur.couleur
                self.creerChar(x,y,0,Vec3(couleur[0],couleur[1],couleur[2]),DTO.joueurs[0].attributs)
            else:
                couleur = joueur.couleur
                self.creerChar(x,y,1,Vec3(couleur[0],couleur[1],couleur[2]),DTO.joueurs[1].attributs) 

        # génération des items
        self.genererItemParInterval(DTO.mapSelectionne.respawnMin,DTO.mapSelectionne.respawnMax)



    def construireDecor(self, camera):
        modele = loader.loadModel("../asset/Skybox/skybox")
        modele.set_bin("background", 0);
        modele.set_two_sided(True);
        modele.set_depth_write(False);
        modele.set_compass();
        verticalRandomAngle = random.randint(0,45)
        modele.setHpr(0,verticalRandomAngle,-90)
        randomGrayScale = random.uniform(0.6,1.2)
        semiRandomColor = Vec4(randomGrayScale,randomGrayScale,randomGrayScale,1)
        modele.setColorScale(semiRandomColor)
        modele.setPos(0,0,0.5)
        #Et oui! Le ciel est parenté à la caméra!
        modele.reparentTo(camera)

    def construirePlancher(self):
        #Optimisation... on attache les objets statiques au même noeud et on utiliser
        #la méthode flattenStrong() pour améliorer les performances.
        self.noeudOptimisation = NodePath('NoeudOptimisation')
        self.noeudOptimisation.reparentTo(render)

        #Construction du plancher
        # On charge les tuiles qui vont former le plancher
        for i in range(0,self.map_nb_tuile_x):
            for j in range(0,self.map_nb_tuile_y):
                modele = loader.loadModel("../asset/Floor/Floor")
                # Reparentage du modèle à la racine de la scène
                modele.reparentTo(self.noeudOptimisation)
                self.placerSurGrille(modele,i, j)

        #Construction du plancher si on tombe
        #Un plan devrait marche mais j'ai un bug de collision en continu...
        shape = BulletBoxShape(Vec3(50,50,5))
        node = BulletRigidBodyNode('Frontfiere sol')
        node.addShape(shape)
        np = render.attachNewNode(node)
        np.setTag("EntiteTankem","LimiteJeu")
        np.setPos(Vec3(0,0,-9.0))
        self.mondePhysique.attachRigidBody(node)

        #Construction de l'aire de jeu sur laquelle on joue
        shape = BulletBoxShape(Vec3(-self.position_depart_x, -self.position_depart_y, 2))
        node = BulletRigidBodyNode('Plancher')
        node.addShape(shape)
        np = render.attachNewNode(node)
        np.setTag("EntiteTankem","Plancher")
        HACK_VALUE = 0.02 #Optimisation de collision, les masques ne marchent pas
        np.setZ(-2.00 - HACK_VALUE)
        self.mondePhysique.attachRigidBody(node)

    def placerSurGrille(self,noeud,positionX, positionY):
        # On place l'objet en calculant sa position sur la grille
        noeud.setX(self.position_depart_x + (positionX+0.5) * self.map_grosseur_carre)
        noeud.setY(self.position_depart_y + (positionY+0.5) * self.map_grosseur_carre)

    def tirerCanon(self, identifiantLanceur, position, direction):
        #Création d'une balle de physique
        someBalle = balle.Balle(identifiantLanceur,self.mondePhysique)
        self.listeBalle.append(someBalle)
        someBalle.projetter(position,direction)

    def tirerMitraillette(self, identifiantLanceur, position, direction):
        #Création d'une balle de physique
        someBalle = balle.Balle(identifiantLanceur,self.mondePhysique)
        self.listeBalle.append(someBalle)
        someBalle.projetterRapide(position,direction)

    def lancerGrenade(self, identifiantLanceur, position, direction):
        #Création d'une balle de physique
        someBalle = balle.Balle(identifiantLanceur, self.mondePhysique)
        self.listeBalle.append(someBalle)
        someBalle.lancer(position,direction)

    def lancerGuide(self, identifiantLanceur, position, direction):
        #Création d'une balle de physique
        someBalle = balle.Balle(identifiantLanceur, self.mondePhysique)
        self.listeBalle.append(someBalle)

        #On définit la position d'arrivé de missile guidé
        noeudDestination = self.listTank[0].noeudPhysique
        if(identifiantLanceur == 0):
            noeudDestination = self.listTank[1].noeudPhysique

        someBalle.lancerGuide(position,noeudDestination)

    def deposerPiege(self, identifiantLanceur, position, direction):
        #Création d'une balle de physique
        someBalle = balle.Balle(identifiantLanceur, self.mondePhysique)
        self.listeBalle.append(someBalle)
        someBalle.deposer(position,direction)

    def tirerShotgun(self, identifiantLanceur, position, direction):
        #Création d'une balle de physique
        someBalle = balle.Balle(identifiantLanceur,self.mondePhysique)
        self.listeBalle.append(someBalle)
        someBalle.projetterVariable(position,direction)

    #####################################################
    #Création des différentes entités sur la carte
    #####################################################

    def creerItem(self, positionX, positionY, armeId):
        #L'index dans le tableau d'item coincide avec son
        #itemId. Ça va éviter une recherche inutile pendant l'éxécution
        itemCourrant = item.Item()
        self.listeItem.append(itemCourrant)
        #On place le tank sur la grille
        self.placerSurGrille(itemCourrant.noeudPhysique,positionX,positionY)
        self.libererEndroitGrille(positionX, positionY,False)
        itemCourrant.initialisationComplete(armeId,self.mondePhysique , lambda : self.libererEndroitGrille(positionX, positionY,True))

    def creerItemHasard(self, positionX, positionY):
        listeItem = ["Mitraillette", "Shotgun", "Piege", "Grenade", "Guide","Spring"]
        itemHasard = random.choice(listeItem)
        self.creerItem(positionX, positionY,itemHasard)

    def creerItemPositionHasard(self):
        #Pas de do while en Python! Beurk...
        randomX = random.randrange(0,self.map_nb_tuile_x)
        randomY = random.randrange(0,self.map_nb_tuile_y)

        #Tant qu'on trouve pas d'endroit disponibles...
        while(not self.endroitDisponible[randomX][randomY]):
            randomX = random.randrange(0,self.map_nb_tuile_x)
            randomY = random.randrange(0,self.map_nb_tuile_y)

        #Quand c'est fait on met un item au hasard
        self.creerItemHasard(randomX,randomY)

    def genererItemParInterval(self, delaiMinimum, delaiMaximum):
        #Délai au hasard entre les bornes
        delai = random.uniform(delaiMinimum, delaiMaximum)
        intervalDelai = Wait(delai)
        intervalCreerItem = Func(self.creerItemPositionHasard)
        intervalRecommence = Func(self.genererItemParInterval,delaiMinimum,delaiMaximum)

        sequenceCreation = Sequence(intervalDelai,
                                    intervalCreerItem,
                                    intervalRecommence,
                                    name="Creation item automatique")
        #On le joue une fois et il se rappelera lui-même :-)
        sequenceCreation.start()

    def creerMur(self,positionX, positionY, strAnimation = None, appendObject = None):
        mur = Wall(self.mondePhysique)
        #On place le bloc sur la grille
        if(appendObject != None):
            #Décale l'objet de 1 unité pour être SUR le mur et non dedans
            appendObject.noeudPhysique.setZ(appendObject.noeudPhysique.getZ() + 1.0)
            appendObject.noeudPhysique.reparentTo(mur.noeudPhysique)
        self.placerSurGrille(mur.noeudPhysique,positionX,positionY)
        self.libererEndroitGrille(positionX,positionY,False)

        if(strAnimation):
            mur.animate(self.dictNoeudAnimation[strAnimation])

    def creerArbre(self,positionX, positionY):
        arbre = Arbre(self.mondePhysique,self.treeOMatic)
        #On place le bloc sur la grille
        self.placerSurGrille(arbre.noeudPhysique,positionX,positionY)
        self.libererEndroitGrille(positionX,positionY,False)

    def creerNoeudAnimationImmobile(self):
        noeudAnimationCourrant = NodePath("AnimationMurImmobile")
        self.dictNoeudAnimation["AnimationMurImmobile"] = noeudAnimationCourrant
        noeudAnimationCourrant.reparentTo(render)

    def creerNoeudAnimationVerticale(self):
        #Création d'un noeud vide
        noeudAnimationCourrant = NodePath("AnimationMurVerticale")
        tempsMouvement = 0.8
        blocPosInterval1 = LerpPosInterval( noeudAnimationCourrant,
                                            tempsMouvement,
                                            Vec3(0,0,-self.map_grosseur_carre + self.map_petite_valeur_carre),
                                            startPos=Vec3(0,0,0))
        blocPosInterval2 = LerpPosInterval( noeudAnimationCourrant,
                                            tempsMouvement,
                                            Vec3(0,0,0),
                                            startPos=Vec3(0,0,-self.map_grosseur_carre + self.map_petite_valeur_carre))
        delai = Wait(1.2)
        # On créé une séquence pour bouger le bloc
        mouvementBloc = Sequence()
        mouvementBloc = Sequence(   blocPosInterval1,
                                    delai,
                                    blocPosInterval2,
                                    delai,
                                    name="mouvement-bloc")

        mouvementBloc.loop()

        noeudAnimationCourrant.reparentTo(render)
        #Ajout dans le dicitonnaire de l'animation
        self.dictNoeudAnimation["AnimationMurVerticale"] = noeudAnimationCourrant

    def creerNoeudAnimationVerticaleInverse(self):
        #Création d'un noeud vide
        noeudAnimationCourrant = NodePath("AnimationMurVerticaleInverse")
        tempsMouvement = 0.8
        blocPosInterval1 = LerpPosInterval( noeudAnimationCourrant,
                                            tempsMouvement,
                                            Vec3(0,0,-self.map_grosseur_carre + self.map_petite_valeur_carre),
                                            startPos=Vec3(0,0,0))
        blocPosInterval2 = LerpPosInterval( noeudAnimationCourrant,
                                            tempsMouvement,
                                            Vec3(0,0,0),
                                            startPos=Vec3(0,0,-self.map_grosseur_carre + self.map_petite_valeur_carre))
        delai = Wait(1.2)
        # On créé une séquence pour bouger le bloc
        mouvementBloc = Sequence()
        mouvementBloc = Sequence(   blocPosInterval2,
                                    delai,
                                    blocPosInterval1,
                                    delai,
                                    name="mouvement-bloc-inverse")
        mouvementBloc.loop()

        noeudAnimationCourrant.reparentTo(render)
        #Ajout dans le dicitonnaire de l'animation
        self.dictNoeudAnimation["AnimationMurVerticaleInverse"] = noeudAnimationCourrant


    def creerChar(self,positionX, positionY, identifiant, couleur,attributs):
        # lorsqu'il n'y a pas de connexion oracle, les valeurs par défaut sont utilisées
        if attributs == None:
            attributs = {"vie":0, "force":0,"agilite":0,"dexterite":0}
        someTank = tank.Tank(identifiant,couleur,self.mondePhysique, attributs)
        #On place le tank sur la grille
        self.placerSurGrille(someTank.noeudPhysique,positionX,positionY)

        #Ajouter le char dans la liste
        self.listTank.append(someTank)

    def traiterCollision(self,node0, node1):
        #Pas très propre mais enfin...
        indiceTank = int(self.traiterCollisionTankAvecObjet(node0, node1,"Balle"))
        if(indiceTank != -1):
            tireurBalleId = int(self.trouverTag(node0, node1, "lanceurId"))
            balleId = int(self.trouverTag(node0, node1, "balleId"))
            #Prend 1 de dommage par défaut si la balle n'a pas été tirée par le tank
            self.listeBalle[balleId].exploser()
            if(tireurBalleId != indiceTank):
                # vérifier que la même balle n'a déjà généré de dommage
                # car pour chaque balle, on ne veut que le compter une fois
                if balleId not in self.listTank[indiceTank].ballesRecus:
                    self.listTank[indiceTank].ballesRecus.append(balleId)
                    #si un joueur recoit du dommage, ca veut dire que l'autre joueur a reussi son tir!
                    #on va donc ajouter les statistiques1 a cet endroit!
                    #note: il faut trouver un moyen pour déterminer c'est quel arme qui est utilisé...
                    nomArmeUtilise =  self.listTank[tireurBalleId].derniereArmeUtilise
                    self.listTank[tireurBalleId].dictStatArme[nomArmeUtilise].ajouterTirReussi()
                    #ajouter les statistiques pour les coups reçus par armes
                    #comme le tank a toujours 2 armes en sa possession, on ajoute les statistiques pour les deux armes
                    victime = 0
                    if tireurBalleId == 0:
                        victime = 1
                    elif tireurBalleId == 1:
                        victime = 0
                    self.listTank[victime].dictStatArme[nomArmeUtilise].ajouterTirRecu()
                #le dommage recu sera en fonction de la force de l'autre joueur
                self.listTank[indiceTank].prendDommage(1 * self.listTank[tireurBalleId].attributs["force"] * 0.05 + 1,self.mondePhysique)


            return
        
        indiceTank = int(self.traiterCollisionTankAvecObjet(node0, node1,"Item"))
        if(indiceTank != -1):
            itemID = int(self.trouverTag(node0, node1, "itemId"))
            if(itemID != -1):
                #Avertit l'item et le tank de la récupération
                itemCourrant = self.listeItem[itemID]
                itemCourrant.recupere()
                self.listTank[indiceTank].recupereItem(itemCourrant.armeId)
                return

        indiceTank = int(self.traiterCollisionTankAvecObjet(node0, node1,"LimiteJeu"))
        if(indiceTank != -1):
            #Un tank est tombé. mouhahahadddddddddd
            self.listTank[indiceTank].tombe(self.mondePhysique)
            return


    #Méthode qui va retourner -1 si aucune collision avec un tank
    #Ou encore l'index du tank touché si applicable
    def traiterCollisionTankAvecObjet(self,node0,node1,testEntite):
        tag0 = node0.getTag("EntiteTankem")
        tag1 = node1.getTag("EntiteTankem")
        retour = -1
        if(tag0 == "Tank" and tag1 == testEntite):
            retour = node0.getTag("IdTank")

        if(tag0 == testEntite and tag1 == "Tank"):
            retour = node1.getTag("IdTank")
        return retour

    #Trouve si un des 2 noeuds a le tag indiqué
    def trouverTag(self,node0, node1, tag):
        retour = ""
        #On trouve l'ID de l'item qui a collisionné
        if(node0.getTag(tag) != ""):
            retour = node0.getTag(tag)

        if(node1.getTag(tag) != ""):
            retour = node1.getTag(tag)

        return retour

    #On met à jour ce qui est nécessaire de mettre à jour
    def update(self,tempsTot):
        for tank in self.listTank:
            tank.traiteMouvement(tempsTot)