#coding: utf-8
#import cx_Oracle
#import id_oracle_account



class DAO():

    def __init__(self):
        self.dto = None
        self.oracle_cursor = None
        

    def connection_oracle(self):
        try:
            self.oracle_connection = cx_Oracle.connect(id_oracle_account.id,id_oracle_account.password,'delta/decinfo.edu')
            self.oracle_cursor = self.oracle_connection.cursor()
    
        except Exception:
            print("la connection n'a pu se faire dans oracle")
    

    def deconnection_oracle(self):
        self.oracle_cursor.close()
        self.oracle_connection.close()

    def mettre_a_jour_oracle(self, dto):
        self.dto
        self.ajouter_joueur_oracle(dto.nom_du_joueur,dto.distance,dto.gagnant,dto.vie,dto.force,dto.agilite,dto.dexterite,dto.phrase_joueur,dto.mot_de_passe,dto.couleurs_tank)

    def ajouter_joueur_oracle(self, nom, distance, gagnant, vie, force, agilite, dexterite, phrase_joueur, mot_de_passe, couleurs):
        v=","
        self.faire_une_requete("INSERT INTO joueur (nom, distance, gagnant,Vie,Force,Agilite,Dexterite, Phrase_Joueur, Mot_De_Passe) "+"VALUES (" +nom+v+distance+v+gagnant+v+vie+v+force+v+agilite+v+dexterite+v+phrase_joueur+v+mot_de_passe+");")
        self.faire_une_requete("INSERT INTO couleur_char(rouge,vert,bleu) VALUES("+self.dto.couleur_tank_rouge+v+self.dto.self.couleur_tank_vert+v+self.dto.couleur_tank_blue+");")
    
    def supprimer_joueur(self, nom_du_joueur):
        try:
        self.faire_une_requete("DELETE FROM joueur WHERE name =" + nom_du_joueur)
        except Exception:
            print("la requete a echoue")

    def verifier_existance_nom_joueur(self, nom_du_joueur):
        resultat =  self.faire_une_requete("SELECT nom = " + nom_du_joueur + " FROM joueur") #Renvoie true ou false dependement du resultat de la requete.   
        return resultat 


    def faire_une_requete(self,sql_statement, confirmation_message = None):
        try:
            self.oracle_cursor.execute(sql_statement)
            if confirmation_message:
                print(u"Requête terminée avec succès : " + confirmation_message)
        except cx_Oracle.DatabaseError as excep:
            error, = excep.args
            print(u"!Erreur d'exécution d'une requête à la base de données!")
            print(" - Error code : " + str(error.code))			# Code de l'erreur pour chercher sur Google
            print(" - Error message : " + str(error.message)) 	# Message du SGBD
            print(" - Error context : " + str(error.context)) 	# Donne la fonction qui a plantée
    # executer(oracle_cursor, "INSERT INTO table_bidon VALUES(1, 2, 3);")