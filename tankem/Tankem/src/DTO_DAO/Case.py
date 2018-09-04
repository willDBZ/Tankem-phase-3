class Case():
	def __init__(self,id_type, colonne, rangee, arbre):
		self.type = id_type
		self.colonne = colonne 
		self.rangee = rangee 
		if (arbre):
			self.arbre = True
		else:
			self.arbre = False