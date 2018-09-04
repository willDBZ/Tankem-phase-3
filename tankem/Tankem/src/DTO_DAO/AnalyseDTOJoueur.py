# -*- coding: utf-8 -*-
import math
import random

 # auteur: William Tang
class AnalyseDTOJoueur():
    dictionnaireAttributA = {"dexterite": ("le précis", "l'habile", "le chirurgien"), 
                            "agilite": ("le prompt", "le lynx", "le foudroyant"),
                            "force": ("le crossfiter", "le hulk", "le tout puissant"),
                            "vie": ("le fougeux", "le pétulant", "l'immortel")
    }

    dictionnaireAttributB = {"dexterite": ("précis", "habile", "chirurgien"), 
                            "agilite": ("prompt", "lynx", "foudroyant"),
                            "force": ("qui fait du crossfit", "brutal", "Marc-André"),
                            "vie": ("fougeux", "pétulant", "immortel")
    }



    def calculerNom(self,DTOJoueur):
        qualificatifA = ""
        qualificatifB = ""
        dominateur = True
        unSeulAttribut = False
        compteurUnSeulAttribut = 0

        #créer une liste temporaire
        # en transformant le dictionnaire en tableau
        listeTempo = []
        for key, value in DTOJoueur.attributs.iteritems():
            if value != 20:
                dominateur = False
            if value == 0:
                compteurUnSeulAttribut = compteurUnSeulAttribut + 1
            listeTempo.append((key,value))
        listeTempo2 = listeTempo[:]

        # le joueur a un seul attribut
        if compteurUnSeulAttribut == 3:
            unSeulAttribut = True
            qualificatifsACalculer = 1
        else:
            qualificatifsACalculer = 2
        
        if not dominateur:
            # determiner l'attribut le plus puissant
            lesPlusForts = []
            
            for j in range(qualificatifsACalculer):
                max = 0
                maxes = []
                for i in range(len(listeTempo)):
                    if listeTempo[i][1] > listeTempo[max][1]:
                        maxes = []
                        max = i
                        maxes.append(listeTempo[max])
                    elif listeTempo[i][1] == listeTempo[max][1]:
                        max = i
                        maxes.append(listeTempo[max])

                # ajouter les attributs les plus forts dans une liste
                lesPlusForts.append(maxes)
                maxValue = listeTempo[max][1]
                for i in range(len(listeTempo)-1,-1,-1):
                    if listeTempo[i][1] == maxValue:
                        listeTempo.pop(i)

                if len(maxes) >= 2:
                    break

            choix = []
            for forts in lesPlusForts:
                while len(forts) != 0:
                    if len(choix) >= 2:
                        break
                    choisi = random.randint(0,len(forts)-1)
                    choix.append(forts[choisi])
                    forts.pop(choisi)



                
            qualificatifA = self.determinerQualificatif(choix[0][1],choix[0][0],0)
            if not unSeulAttribut:
                qualificatifB = self.determinerQualificatif(choix[1][1],choix[1][0],1)
            nomCalcule = DTOJoueur.nom + " " + qualificatifA + " " + qualificatifB
        else:
            nomCalcule = "Dominateur " + DTOJoueur.nom
        return nomCalcule



    def joueurLePlusFort(self,joueur1, joueur2):
        if self.calculerLevel(joueur1) > self.calculerLevel(joueur2):
            return joueur1
        elif self.calculerLevel(joueur1) < self.calculerLevel(joueur2):
            return joueur2
        else:
            return None

    def determinerQualificatif(self, nbCoolPoints, attribut,ordre):
        if ordre == 0:
            dico = self.dictionnaireAttributA[attribut]
        elif ordre == 1:
            dico = self.dictionnaireAttributB[attribut]

        if nbCoolPoints >= 10:
            qualificatif= dico[2]
        elif nbCoolPoints >= 5:
            qualificatif= dico[1]
        else:
            qualificatif = dico[0]

        return qualificatif