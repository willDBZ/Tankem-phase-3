# -*- coding: utf-8 -*-

import cx_Oracle
import id_oracle_account
from DTO import DTO
from LookupTable import LookupTable
from DAO_Balance import DAO_Balance
from Map import Map
from Case import Case
from Joueur import Joueur
import datetime
from DTO_DAO.Sanitizer import Sanitizer

 # auteur: William Tang
class DAO_Oracle(DAO_Balance):
	__logger_instance = None

	def __new__(cls):
		if not DAO_Oracle.__logger_instance:
			DAO_Oracle.__logger_instance = DAO_Oracle.__InternalDAO()
			DAO_Oracle.__logger_instance.connectDB()
		return DAO_Oracle.__logger_instance

	class __InternalDAO(object):
		

		def connectDB(self):
			try:
				# général: pour coder à l'école
				self.oracle_connection = cx_Oracle.connect(id_oracle_account.id,id_oracle_account.password,'delta/decinfo.edu')
				self.oracle_cursor = self.oracle_connection.cursor()
				DTO.etatConnexionOracle = True
			except Exception:
				DTO.etatConnexionOracle = False

			return DTO.etatConnexionOracle

		def getConnexionState(self):
			return DTO.etatConnexionOracle

		

		def __disconnect_from_DB(self):
			self.oracle_cursor.close()
			self.oracle_connection.close()
		
		def __execute_query(self,cursor, sql_statement, confirmation_message = None):
			try:
				# if (values == {}):
				print sql_statement
				cursor.execute(sql_statement)

				# else:
				# 	cursor.execute(sql_statement,values)
				
				if confirmation_message:
					print(u"Requête terminée avec succès : " + confirmation_message)
			except cx_Oracle.DatabaseError as excep:
				error, = excep.args
				print(u"!Erreur d'exécution d'une requête à la base de données!")
				print(" - Error code : " + str(error.code))			# Code de l'erreur pour chercher sur Google
				print(" - Error message : " + str(error.message)) 	# Message du SGBD
				print(" - Error context : " + str(error.context))  

		def fill_dto_with_db(self):
			table_name = "Map"
			self.__execute_query(self.oracle_cursor, "SELECT * FROM %s WHERE id_status = 1 and id != -1 ORDER BY titre" %(table_name))
			query_result = self.oracle_cursor.fetchall()     
			for row in query_result:
				DTO.maps.append(Map(row[0],row[1],row[2],row[3],row[4], row[5], row[6],row[7]))

		def fillLookupTableArmes(self):
			# une lookuptable qui permet de rapidement associer le nom d'une arme à son id
			# utile lors des insertion des données à la fin de la partie, pour les statistiques sur les armes
			# {"vie":vie, "force":force,"agilite":agilite,"dexterite":dexterite}
			table_name = "Armes"
			self.__execute_query(self.oracle_cursor, "SELECT * FROM %s" %(table_name))
			query_result = self.oracle_cursor.fetchall()     
			for row in query_result:
				LookupTable.tableArmes[row[1]] = row[0]

		def selectSomething(self, sql):
			# remplir les cases
			# table_name = "Cases"
			self.__execute_query(self.oracle_cursor, sql)
			query_result = self.oracle_cursor.fetchall()  

			for row in query_result:
				return row[0]
			return None

		def fillGame(self, idMap):
			# la map sélectionnée
			for i in range(len(DTO.maps)):
				if DTO.maps[i].id == idMap:
					DTO.mapSelectionne = DTO.maps[i]
					DTO.idMap = idMap

			if DTO.mapSelectionne != None:

				# remplir les cases
				table_name = "Cases"
				self.__execute_query(self.oracle_cursor, "SELECT * FROM %s WHERE id_map = %d" %(table_name, idMap))
				query_result = self.oracle_cursor.fetchall()  

				nbRangees = DTO.mapSelectionne.rangees
				for row in query_result:
					rangeeCorrectif = nbRangees-1-row[4]
					DTO.cases.append(Case(row[1], row[2], row[3], rangeeCorrectif))

				#william cette partie de code n'est plus nécessaire pour la phase 3
				# remplir les joueurs
				table_name = "Joueur_map"
				self.__execute_query(self.oracle_cursor, "SELECT * FROM %s WHERE id_map = %d order by ordre" %(table_name, idMap))
				query_result = self.oracle_cursor.fetchall() 

				index = 0    
				for row in query_result:
					DTO.joueurs[index].x = row[1]
					DTO.joueurs[index].y = row[2]
					index = index + 1
			
		def validerUsager(self, usager, password,ordre):
			table_name = "joueur"
			# vérifier s'il y a un résultat (impossible qu'il y en ait plus qu'un)
			sql = "SELECT * FROM %s WHERE NOM = '%s' AND MOT_DE_PASSE = '%s'" %(table_name, usager, password)
			self.__execute_query(self.oracle_cursor, sql)
			query_result = self.oracle_cursor.fetchall()
			connecte = False     
			for row in query_result:
				connecte = True				
				nouveauJoueur = Joueur(1,1,ordre,row[1],(row[9],row[10],row[11]), row[7], row[8], row[2], row[3],row[4],row[5],row[0], row[6])
				sanitizer = Sanitizer()
				if ordre == 0:
					DTO.joueur1 = nouveauJoueur
					DTO.joueur1,DTO.messagesErreurs1 = sanitizer.checkDTO(DTO.joueur1)
				elif ordre == 1:
					DTO.joueur2 = nouveauJoueur
					DTO.joueur2,DTO.messagesErreurs2 = sanitizer.checkDTO(DTO.joueur2)

				if DTO.joueur1 and DTO.joueur2:
					DTO.joueurs.append(DTO.joueur1)
					DTO.joueurs.append(DTO.joueur2)
			return connecte

		def insertFin_PartieProcedure(self, date_debut, date_fin, id_map, id_joueur1, id_joueur2, distance1, distance2,experience1,experience2):
			partie_joueur_id = []
			partie_joueur_id.append(self.oracle_cursor.var(cx_Oracle.NUMBER))
			partie_joueur_id.append(self.oracle_cursor.var(cx_Oracle.NUMBER))
			self.oracle_cursor.callproc("insertFin_PartieProcedure",[date_debut, date_fin, id_map, id_joueur1, id_joueur2, distance1, distance2,experience1,experience2,partie_joueur_id[0],partie_joueur_id[1]]) 

			return partie_joueur_id

		def insertArmes_StatProcedure(self,id_arme,Coup_Tire_Atteint_Cible,Coup_Recu,Coup_Total,partie_Joueur_id):
			# id_arme IN INTEGER, Coup_Tire_Atteint_Cible IN INTEGER,Coup_Recu IN INTEGER, Coup_Total IN INTEGER, partie_Joueur_id IN INTEGER
			self.oracle_cursor.callproc("insertArmes_StatProcedure",[id_arme,Coup_Tire_Atteint_Cible,Coup_Recu,Coup_Total,partie_Joueur_id]) 
		 	
			

		def envoyerStatistiques(self):
			# insertion d'une statistique pour une nouvelle partie jouée
			if DTO.joueurs[0].vainqueur:
				gagnant = DTO.joueurs[0]
				perdant = DTO.joueurs[1]
			else:
				gagnant = DTO.joueurs[1]
				perdant = DTO.joueurs[0]

			# si l'id_map est null, alors c'est une map aléatoire
			now =  datetime.datetime.now()
			if (DTO.idMap == None):
				DTO.idMap = -1
			partie_joueur_id = self.insertFin_PartieProcedure(now,now, DTO.idMap,gagnant.id, perdant.id, gagnant.tank.distance, perdant.tank.distance,gagnant.experience, perdant.experience)
			
			for i in range(len(DTO.joueurs)):
				joueur = DTO.joueurs[i]
				# # insertion des nouvelles données du joueur
				statArmes = joueur.tank.dictStatArme
				for key, arme in statArmes.iteritems():
					self.insertArmes_StatProcedure(LookupTable.tableArmes[key],arme.tirReussi,arme.tirRecu,arme.tirTotal, partie_joueur_id[i])
			
			# on fait un envoie dans la bd seulement s'il n'y a pas eu aucune erreur
			self.oracle_connection.commit()