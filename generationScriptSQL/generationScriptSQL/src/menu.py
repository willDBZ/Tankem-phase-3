## -*- coding: utf-8 -*-
# technique d'écriture de fichier texte
# https://www.guru99.com/reading-and-writing-files-in-python.html#1

import sys
from random import randint
import random



class Menu():

    def __init__(self):
        print('Bienvenu dans l ajout du joueur')
        self.menu()

# Ajout d'un nom de joueur ainsi que l'insertion de celui-ci dans la procedure

    def ajout_joueur(self):
         print("vous avez choisi l'option d'ajout d'un joueur")
         joueurs = []
        
         couleur= random.randint(0,255)
         coolpoint = random.randint(0,2)
         insertion_variables = "var id_joueur1 number;\n\rvar id_joueur2 number;\n\r"

         for x in range (0,4):
             reponseJ = raw_input("Entrer votre nom de joueur:")
        
             joueurs.append(reponseJ[:-1])
             


         fichier= open("insertionStatistique.sql","w")
         fichier.write(insertion_variables)
         

         
        # insertion des joueurs
         for x in range(0, 3):
                fichier= open("insertionStatistique.sql","a+")
                sql = "execute insertJoueurProcedure('%s','%d','%d','%d','%d','Je suis le Boss','1',0,'%s','%s','%s');\r\n"%(joueurs[x],coolpoint,
                coolpoint,coolpoint,coolpoint,couleur,couleur,couleur)
                fichier.write(sql)

         for y in range(0,250):

            self.insertion_partie()
            for q in range(0,2):
                for z in range(0,8):
                    self.insertion_armes()
           
         fichier.close()

    def menu(self):

        print("Option 1 ajout d'un joueur")
        print("Option 2 quitter")

        reponse = input("Choisissez une option:")

        if reponse == 1:
            self.ajout_joueur()
        elif( reponse == 2):
            sys.exit()

        else:
            print("Erreur option non valide reessayer")
            self.menu()
    

    # permet l'insertion de 250 partie
    def insertion_partie(self):

         #for i in range(1,250):

            self.joueur1 = random.randint(1, 3)

            self.joueur2 = random.randint(1, 3)
            


            while (self.joueur2 == self.joueur1):

                self.joueur2 = random.randint(1, 3)



            if(random.randint(0, 100) >= 50):

             self.gagnant = self.joueur1

            else:

             self.gagnant = self.joueur2


            moisaleatoire = random.randint(1, 12)

            champMois = ""

            if (moisaleatoire > 9):

                champMois = str(moisaleatoire)

        #si le mois est plus petit que 9 ajout d'un 0 (pour la cohérence avec la  BD)
            else:

                champMois = "0" + str(moisaleatoire)

            anneealeatoire = str(random.randint(2015, 2018))

            jouraleatoire = 0


        # si mois est fevrier
            
            if(moisaleatoire == 2):

                jouraleatoire = random.randint(1, 28)

        # si le mois est pair
         
            elif(moisaleatoire % 2 == 0):

                jouraleatoire = random.randint(1, 30)

            else:

                jouraleatoire = random.randint(1, 31)

            if(moisaleatoire ==9):
                jouraleatoire = random.randint(1,30)

            elif(moisaleatoire == 7):
                jouraleatoire = random.randint(1,31)
            
            elif(moisaleatoire == 8):
                jouraleatoire = random.randint(1,31)

            if (jouraleatoire >= 9):

                champJour = str(jouraleatoire)

            else:

                champJour = "0" + str(jouraleatoire)


            date_alea = str(random.randint(15,40))
            

    #execute insertFin_PartieProcedure(TO_DATE('2018/05/24 10:10:10', 'yyyy/mm/dd hh24:mi:ss'),TO_DATE('2018/05/24 10:10:10', 'yyyy/mm/dd hh24:mi:ss') + 34, 3, 1, 3, 4932, 1160, 277, 351,:id_joueur1,:id_joueur2);
        # appel de procedure avec les dates aleatoires 

            id_joueur1 = "id_joueur1"
            id_joueur2 = "id_joueur2"
           
            insertion_jeux = "execute insertFin_PartieProcedure(%s,%s, %d, %d, %d, %d, %d, %d, %d,:%s,:%s);\n\r" %("TO_DATE('"+ anneealeatoire +"/"+ champMois +"/"+ champJour + " 10:10:"+ date_alea + "', 'yyyy/mm/dd hh24:mi:ss')",
            "TO_DATE('"+ anneealeatoire +"/"+ champMois +"/"+ champJour +" 10:12:10', 'yyyy/mm/dd hh24:mi:ss')", 
            random.randint(1,3),
            int(self.joueur1),
            int(self.joueur2),
            random.randint(1000,5000),
            random.randint(1000,5000),
            random.randint(200,500),
            random.randint(200,500),id_joueur1,id_joueur2)

            fichier= open("insertionStatistique.sql","a+")
            fichier.write(insertion_jeux)
    
    
    # permet l'insertion des armes (en fonction des 250 parties pour 2 joueurs, 8 armes chacun)
    def insertion_armes(self):

        #for x in range(0,250):

            #for y in range(0,2):

                 #for a in range(0,8):

                        insertion_variables = "var id_joueur1 number;\n\r#var id_joueur2 number;"
                        id_joueur = ["id_joueur1","id_joueur2"]

                        choix = random.choice(id_joueur)

                        coup_total = random.randint(0,100)
                        choix_armes = random.randint(1,8)
                        coup_recu = random.uniform(0.7, 0.9)*coup_total
                        coup_tirer_atteint_cible = random.uniform(0.7,0.9)*coup_total
                        partie_joueur_id = random.randint(0,2)

                        sql_stat = "execute insertArmes_StatProcedure('%d','%d','%d','%d', :%s);\n\r"%(choix_armes,coup_tirer_atteint_cible,coup_recu,coup_total,choix)
                
                        fichier= open("insertionStatistique.sql","a+")
                        fichier.write(sql_stat)