# -*- coding: utf-8 -*-

class Message():
    def __init__(self,typeDonnee,champ,ancienneValeur,nouvelleValeur):
        self.typeDonnee = typeDonnee
        self.champ = champ
        self.ancienneValeur = ancienneValeur
        self.nouvelleValeur = nouvelleValeur

    def retournerMessage(self):
        message = "%s pour %s du joueur qui était de %s a été changé pour %d."%(self.typeDonnee, self.champ,  "{0:.2f}".format(self.ancienneValeur), self.nouvelleValeur)
        return message