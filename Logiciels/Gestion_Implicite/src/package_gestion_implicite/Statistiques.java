package package_gestion_implicite;

import java.sql.SQLException;

/*Classe qui fait des calculs à partir des résultats obtenus de la classe dto afin de faire des statitiques qui seront affichées par la classe Editeur .*/

public class Statistiques {
	private String nom_du_joueur;
	
	private DTO dto;
	
	public Statistiques(String nom_du_joueur){
		this.dto=dto;
	}

	
	public Statistiques(DTO dto){
		this.dto=dto;
	}
	
	

}
