package package_gestion_implicite;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Vector;

import oracle.jdbc.pool.OracleDataSource;

public class DAO {
	
	private static Connection conn;
	private String jdbcUrl = null;
	private String userid = null;
	private String password = null; 
	private DTO dto; 
	private Initialise_DTO initialiseur_dto;
	
	
	public DAO() throws SQLException{
		
		if(conn != null) {
			this.getDBConnection();
			System.out.print("Déja connecté");
		}
		else {
			 OracleDataSource ds = new OracleDataSource();
		     ds.setURL("jdbc:oracle:thin:@delta:1521:decinfo");
		     conn = ds.getConnection("e1072359","Delm14059209");  
		     System.out.print("première connexion réussie!");
		}
		
		dto = new DTO();
		

	}
	
	public Connection getDBConnection() {
	      return conn;
		
	}
	
	public Boolean verifier_credentiels_utilisateur(String nom_du_joueur, String mot_de_passe) throws SQLException{  // Vérifie que le joueur exite dans la base de donné et que son mot de passe est correct. 
	
		ResultSet resultats;
		
			resultats = Faire_une_requete("select nom, mot_de_passe from joueur where nom =" + "'" + nom_du_joueur + "'");
		
		if(resultats.next()){ 
			String nom = resultats.getString("nom");
			String mdp = resultats.getString("mot_de_passe");
			
			if(mdp.equals(mot_de_passe)){
				dto.setNom_du_joueur(nom_du_joueur);
				initialiseur_dto = new Initialise_DTO(dto);
				initialiseur_dto.init_DTO(); 				// Sert a remplir le dto 
				return true;                             // Si le nom et le mot de passe sont valides 
			}
			else if(mdp != mot_de_passe){
				return false;                             // Si le mot le mot de passe n'est pas valide
			}
		}
		else if(!resultats.next()){  // si aucun résultat n'est retourné  donc si l'alias n'existe pas 
			System.out.println("L'alias entré n'existe pas.");
			return false;
		}
		
		return false;
		
	}
	
	public ResultSet Faire_une_requete(String query) throws SQLException{
        getDBConnection(); 
        Statement stmt = conn.createStatement(ResultSet.TYPE_SCROLL_SENSITIVE,ResultSet.CONCUR_READ_ONLY);
        System.out.println("\nExecuting query: " + query);
        ResultSet rset = stmt.executeQuery(query); 
        return rset;
    }
	
	
	private DTO get_dto(){
		return this.dto;
	}
	
	private class Initialise_DTO{
	/*Classe dans laquelle on va faire des sélect pour remplir les champs voulus dans le dto.*/
		private DTO dto;
		private String nom_du_joueur;
		
		public Initialise_DTO(DTO dto){
			this.dto = dto;
			nom_du_joueur = dto.getNom_du_joueur();
		}
		
		public void init_DTO() throws SQLException{   // Début de la chaine de fonctions qui rempliront le DTO 
			charger_coolpoints();
			charger_phrase_du_joueur();
			charger_couleurs_tank_joueur();
			charger_experience();
			//charger_armes();
			charger_nombre_parties_total();
		}
		
		
		
		
		public DTO get_DTO(){
			return this.dto;
		}
		
		
		private void charger_phrase_du_joueur()throws SQLException{
			String requete = "Select phrase_joueur from joueur where nom ="+ "'"+ nom_du_joueur + "'";
			ResultSet resultat = Faire_une_requete(requete);
			while(resultat.next()){
				dto.setPhrase_du_joueur(resultat.getString("phrase_joueur"));
			}
		}
		
		private void charger_couleurs_tank_joueur()throws SQLException{
			String requete = "Select rouge,vert,bleu from joueur where nom = " + "'" + nom_du_joueur + "'";
			ResultSet resultat = Faire_une_requete(requete);
			while(resultat.next()){
				dto.setCouleur_tank_rouge(resultat.getInt("rouge"));
				dto.setCouleur_tank_vert(resultat.getInt("vert"));
				dto.setCouleur_tank_bleu(resultat.getInt("bleu"));
			}
		}
		
		private void charger_experience()throws SQLException{
			String requete = "Select experience from joueur where nom = " + "'" + nom_du_joueur + "'";
			ResultSet resultat = Faire_une_requete(requete);
			while(resultat.next()){
				dto.setExperience(resultat.getInt("experience"));
			}
			
		}
		
		private void charger_coolpoints()throws SQLException{
			String requete = "Select vie,force,agilite,dexterite from joueur where nom = "+ "'" + nom_du_joueur +"'"; 
			ResultSet resultat = Faire_une_requete(requete);
			while(resultat.next()){
				dto.setCoolpoints_vie(resultat.getInt("vie"));
				dto.setCoolpoints_force(resultat.getInt("force"));
				dto.setCoolpoints_agilite(resultat.getInt("agilite"));
				dto.setCoolpoints_dexterite(resultat.getInt("dexterite")); 
			}
			
			
		}
		
		private void charger_armes()throws SQLException{
			Vector<String> armes = new Vector<String>();
			String requete = "Select nom from armes where id = (Select id_partie_joueur from armes_stat where id=(select id_joueur from partie_joueur where id = (select id from joueur where nom = "+"'"+nom_du_joueur+"'"+ ")))";
			ResultSet resultat = Faire_une_requete(requete);
			while(resultat.next()){
				armes.add(resultat.getString("nom"));
			}
		}
		
		private void charger_nombre_parties_total()throws SQLException{
			int nombre_parties_total;
			String requete = "SELECT COUNT(id_joueur) FROM partie_joueur where id =(select id from joueur where nom ="+"'"+nom_du_joueur+"'" +")";
			ResultSet resultat = Faire_une_requete(requete);
			while(resultat.next()){
				dto.setTotal_parties_jouees(resultat.getInt("id_joueur"));
			}
		}

		
	}

	
	
	
	
	private class Update_DTO{
	/*Classe dans laquelle on va faire des inserts pour mettre a jour la BD à la fin du programme*/
	}
	
	
	

}
