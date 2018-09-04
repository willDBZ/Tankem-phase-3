## -*- coding: utf-8 -*-
from DTO_DAO.Message import Message
from DTO_DAO.DTO import DTO
import math
from decimal import *

class Sanitizer():
    def checkDTO(self,dto):
        messages = []

        # la somme des coolpoints doit correspondre au niveau du joueur
        somme = 0
        for key, value in dto.attributs.iteritems():
            somme = somme + value


        limite = dto.level * 5
        if (somme > limite):
            ratio = float(limite) / float(somme)
            # rajuster les valeurs de chaque attributs
            # pour que la somme des coolpoints soit au-dessous de la limite
            for key, value in dto.attributs.iteritems():
                dto.attributs[key] = math.floor(float(value) * float(ratio))

            # dto.vie = math.floor(dto.vie * ratio)
            # dto.force = math.floor(dto.vie * ratio)
            # dto.agilite = math.floor(dto.vie * ratio)
            # dto.dexterite = math.floor(dto.vie * ratio)
            messages.append(Message("La valeur", "le nombre de CoolPoints", somme, limite))

        # le nom du joueur ne doit pas dépasser 15 caractères
        limite = 15
        ancienneValeur = len(dto.nom)
        if (ancienneValeur > limite):
            dto.nom = dto.nom[:limite]
            messages.append(Message("La longueur", "le nom", ancienneValeur, limite))


        # le nombre d'expérience ne doit pas être négatif
        limite = 0
        ancienneValeur = dto.experience
        if (ancienneValeur < limite):
            dto.experience = ancienneValeur
            messages.append(Message("La valeur", "l'expérience", ancienneValeur, limite))

        # la longueur du message du joueur
        limite = 25
        ancienneValeur = len(dto.message)
        if (ancienneValeur > limite):
            dto.message = dto.message[:limite]
            messages.append(Message("La longueur", "le message", ancienneValeur, limite))
        
        # pour les couleurs RGB du tank du joueur
        # comme dans la classe Joueur une fonction est utilisée pour convertir la couleur
        # de 0-255 à 0-1, on va s'assurer que la couleur entre dans ces deux extrémités 
        couleurs = ['R','G','B']
        for i in range(len(dto.couleur)):
            # limite inférieure
            limite = 0
            # ancienneValeur = dto.couleur[i]
            ancienneValeur = float("{0:.2f}".format(dto.couleur[i]))
            if (ancienneValeur < limite):
                dto.couleur[i] = limite
                messages.append(Message("La valeur", "la couleur %s"%(couleurs[i]), ancienneValeur, limite))

            # limite supérieure
            limite = 1
            ancienneValeur = dto.couleur[i]
            if (ancienneValeur > limite):
                dto.couleur[i] = limite
                messages.append(Message("La valeur", "la couleur %s"%(couleurs[i]), ancienneValeur, limite))

        
        # les valeurs des coolpoints doivent être compris entre 0-20
        # valeurs supérieures

        limite = 20
        for key, value in dto.attributs.iteritems():
            ancienneValeur = dto.attributs[key]
            if (ancienneValeur > limite):
                dto.attributs[key] = limite
                messages.append(Message("La valeur", "la %s "%(key), ancienneValeur, limite))
        
        # limite = 20
        # ancienneValeur = dto.vie
        # if (ancienneValeur > limite):
        #     dto.vie = limite
        #     messages.append(Message("La valeur", "la vie ", ancienneValeur, limite))

        # limite = 20
        # ancienneValeur = dto.force
        # if (ancienneValeur > limite):
        #     dto.force = limite
        #     messages.append(Message("La valeur", "la force ", ancienneValeur, limite))

        # limite = 20
        # ancienneValeur = dto.agilite
        # if (ancienneValeur > limite):
        #     dto.agilite = limite
        #     messages.append(Message("La valeur", "la agilite ", ancienneValeur, limite))

        # limite = 20
        # ancienneValeur = dto.dexterite
        # if (ancienneValeur > limite):
        #     dto.dexterite = limite
        #     messages.append(Message("La valeur", "la dexterite ", ancienneValeur, limite))


        # valeurs inférieures
        limite = 0
        for key, value in dto.attributs.iteritems():
            ancienneValeur = dto.attributs[key]
            if (ancienneValeur < limite):
                dto.attributs[key] = limite
                messages.append(Message("La valeur", "la %s "%(key), ancienneValeur, limite))


        # limite = 0
        # ancienneValeur = dto.vie
        # if (ancienneValeur < limite):
        #     dto.vie = limite
        #     messages.append(Message("La valeur", "la vie ", ancienneValeur, limite))

        # limite = 0
        # ancienneValeur = dto.force
        # if (ancienneValeur < limite):
        #     dto.force = limite
        #     messages.append(Message("La valeur", "la force ", ancienneValeur, limite))

        # limite = 0
        # ancienneValeur = dto.agilite
        # if (ancienneValeur < limite):
        #     dto.agilite = limite
        #     messages.append(Message("La valeur", "la agilite ", ancienneValeur, limite))

        # limite = 0
        # ancienneValeur = dto.dexterite
        # if (ancienneValeur < limite):
        #     dto.dexterite = limite
        #     messages.append(Message("La valeur", "la dexterite ", ancienneValeur, limite))


        # après avoir fait toutes les vérifications, on renvoie le dto modifié à la classe DTO
        return (dto,messages)