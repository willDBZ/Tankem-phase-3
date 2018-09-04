#coding: utf-8
from DAO import DAO
from DTO import DTO
import sys

class Gestion_Explicite():

    def __init__(self):
        #dao = DAO()
        #self.connexion_oracle()
        dto = DTO()
        print("Bienvenu dans le logitiel de gestion explicite des joueurs")
        self.menu()

    def ajouter_joueur(self): #Permet d'entrer un alias pour un nouveau joueur 
        print("vous avez choisi d'ajouter un joueur. ")
        dto.nom_du_joueur = input("entrez l'alias voulu pour le nouveau joueur")
        if self.verifier_existance_nom_joueur(dto.nom_du_joueur):
            self.creer_mot_de_passe_joueur(dto.nom_du_joueur)
        else:
            print("Le nom que vous avez entre n'est pas disponible")
            self.ajouter_joueur() # Récursion tant que le nom du joueur n'est pas choisi 

        
    def verifier_existance_nom_joueur(self, nom_du_joueur): # Vérifie que le nom du joueur ne se trouve pas deja dans la base de donnee
        return dao.verifier_existance_nom_joueur(nom_du_joueur)


    def supprimer_joueur(self): # communique avec la bd pour supprimer le joueur
        print("Vous avez choisi de supprimer un joueur .")
        nom_du_joueur_a_supprimer = input("Entrez le nom du joueur que vous desirez supprimer : ")
        print("Vous avez choisi de supprimer " + nom_du_joueur_a_supprimer)
        if(self.verifier_existance_nom_joueur(nom_du_joueur_a_supprimer)== False):
            print(' " ' + nom_du_joueur_a_supprimer + ' " ' + "n'existe pas." )
            reponse = input("Voulez vous reessayer o/n ?")
            if(reponse == 'o'):
                self.supprimer_joueur()
            else:
                self.menu()
        elif(self.verifier_existance_nom_joueur(nom_du_joueur_a_supprimer) == true):
            dao.supprimer_joueur(nom_du_joueur_a_supprimer)


    def creer_mot_de_passe_joueur(self, nom_du_joueur): # Cre le joueur avec toutes ses caractéritiques 
        print("Votre Alias est " + nom_du_joueur)
        dto.mot_de_passe = input("Veuillez choisir un mot de passe pour votre joueur et appuyez sur 'Entrer'.")
        confirmation_mot_de_passe = input("Veuillez confirmer le mot de passe et appuyez sur 'Entrer' . ")
        if(dto.mot_de_passe != confirmation_mot_de_passe):
            print("Les deux mots de passes entrés sont différents, veuillez entrer le meme mot de passe deux fois .")
            dto.mot_de_passe = None
            creer_mot_de_passe_joueur(nom_du_joueur) #Recursion jusqu'a ce que le bon mot de passe soit entré
        elif(dto.mot_de_passe == self.confirmation_mot_de_passe):
            print("Maintenant" + nom_du_joueur + ", il est temps de personnaliser votre tank.")
            self.creer_tank_joueur()

    def creer_phrase_personnelle_Joueur(self):
        print("Voici le moment tant attendu! Choisissez-vous une phrase personelle")
        dto.phrase_personnelle = input("Phrase personnelle : ")
        print("Votre phrase personnelle est : " + dto.phrase_personnelle)
        reponse_changement_phrase = input("Desirez-vous la modifier o/n ?")
        if(reponse_changement_phrase == "o"):
            self.creer_phrase_personnelle_Joueur()
        else:
            self.mettre_a_jour_oracle()
            self.deconnection_oracle()
            self.menu()
        


    def creer_tank_joueur(self):
        print("Les couleurs sont en format RGB. Veuillez entrez un numero entre 0 et 255 pour chaque teinte. Appuyer sur 'Entrer' entre chaque teinte ")
        dto.couleur_tank_rouge = input("Rouge : ")
        dto.couleur_tank_vert = input("Vert : ")
        dto.couleur_tank_bleu = input("Bleu : ")
        for couleur in dto.couleurs_tank:
            if(couleur > 0 or couleur < 255):
                print("Une ou plusieurs des valeurs que vous avez entré est invalide.")
                creer_tank_joueur()



    def menu(self):
        print("Pour ajouter un joueur, faites le 1")
        print("Pour supprimer un joueur, faites le 2")
        print("Pour quitter, faites le q")
        
        reponse = input()

        if(reponse == "1"):
            self.ajouter_joueur()
        elif(reponse == "2"):
           self.supprimer_joueur()
        elif(reponse == 'q'):
            self.deconnection_oracle()
            sys.exit()
        
        else:
            print("vous avez fait un choix non-valide")
            self.menu()


    def connexion_oracle(self):
        dao.connection_oracle()

    def deconnection_oracle(self):
        dao.deconnection_oracle()

    def mettre_a_jour_oracle(self):
        dao.ajouter_joueur_oracle(self.dto)




