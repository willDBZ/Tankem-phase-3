 # auteur: William Tang
class StatArmes():
	tirReussi = 0
	tirTotal = 0
	tirRecu = 0
	
	def __init__(self,id):
		self.id = id

	def ajouterTirReussi(self):
		self.tirReussi +=1

	def ajouterTirTotal(self):
		self.tirTotal +=1

	def ajouterTirRecu(self):
		self.tirRecu +=1