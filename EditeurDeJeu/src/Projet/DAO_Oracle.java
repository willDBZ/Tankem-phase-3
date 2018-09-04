package Projet;
// oracle
//
import java.sql.*;

public class DAO_Oracle extends DAO_Balance {
	public static Connection conn = null;
	public static void main(String [] args)
	{
		connexion();
		insertionDansLaBD();
		deconnexion();
	}	
	
	public static boolean connexion()
	{
		try
		{
			conn = DriverManager.getConnection("jdbc:oracle:thin:@delta:1521:decinfo", "e1072359", "Delm14059209");
			return true;
			
		} catch (Exception e)
		{
			System.out.println(e);
			return false;
		}
	}
	
	public static boolean deconnexion()
	{
		try {
			conn.close();
			return true;
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return false;
		}
	}
	
	public static ResultSet executeStatement(PreparedStatement stmt)
	{
		// Statement stmt;
		try {
			// stmt = conn.createStatement();
			// ResultSet rs = stmt.executeQuery(query);
			ResultSet rs = stmt.executeQuery();
			return rs;
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		return null;
	}
	
	public static int rechercheId(PreparedStatement statement)
	{
		try {				
			ResultSet rs = executeStatement(statement);
			while (rs.next())
			{
				int id = rs.getInt("ID");
				return id;
			}
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		
		
		return -1;
	}
	
	public static boolean insertionDansLaBD()
	{
		PreparedStatement statement;
		int idStatut = -1;
		try {
			statement = conn.prepareStatement(
					"SELECT ID FROM STATUS WHERE NOM = ?"
					);
			statement.setString(1, DTO.getStatut());
			idStatut = rechercheId(statement);
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return false;
		}
		
		
		
		
		// insertion dans la map
		try {
			statement = conn.prepareStatement(
					"INSERT INTO MAP(TITRE,COLONNES,RANGEES,ID_STATUS,DATECREATION, RESPAWN_MIN, RESPAWN_MAX) VALUES(?,?,?,?,sysdate,?,?)"
					);
			statement.setString(1, DTO.getTitre());
			statement.setInt(2, DTO.getNbColonne());
			statement.setInt(3, DTO.getNbLigne());			
			statement.setInt(4, idStatut);
			statement.setDouble(5, DTO.getDelaiApparitionMin());
			statement.setDouble(6, DTO.getDelaiApparitionMax());
			
			executeStatement(statement);
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return false;
		}
		
		
		//id de la map
		int idMap = -1;
		try {
			statement = conn.prepareStatement(
					"SELECT ID FROM MAP WHERE TITRE = ?"
					);
			statement.setString(1, DTO.getTitre());
			idMap = rechercheId(statement);
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return false;
		}
		

		// insertion des cases
		for (int col =0; col < DTO.getNbColonne(); col++)
		{
			for (int row = 0; row < DTO.getNbLigne(); row++)
			{
				Case uneCase = DTO.getCases()[col][row];
				
				if (uneCase.getType() == null)
				{
					uneCase.setType("plancher");
				}
				
				if (!(uneCase.getType() == "plancher" && !uneCase.withArbre()))
				{
						
					
					//id du type
					int idType = -1;
					try {
						statement = conn.prepareStatement(
								"SELECT ID FROM TYPE WHERE NOM = ?"
								);
						statement.setString(1, DTO.getCases()[col][row].getType());
						idType = rechercheId(statement);
					} catch (SQLException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					}
					
					
	
					try 
					{
	
						statement = conn.prepareStatement(
								"INSERT INTO CASES(ID_MAP,ID_TYPE,COLONNE,RANGEE,ARBRE) VALUES(?,?,?,?,?)"
								);
						statement.setInt(1, idMap);
						statement.setInt(2, idType);
						statement.setInt(3, DTO.getCases()[col][row].getCol());			
						statement.setInt(4, DTO.getCases()[col][row].getRow());
						int arbre = 0;
						if (DTO.getCases()[col][row].withArbre())
						{
							arbre = 1;
						}
						statement.setInt(5, arbre);
						
						executeStatement(statement);
					} 
					catch (SQLException e) 
					{
						// TODO Auto-generated catch block
						e.printStackTrace();
						return false;
					}
				}
			}	
		}		
		
		// insertion des joueurs
		for (int i = 0; i < DTO.getJoueurs().length; i++)
		{
			try {
				statement = conn.prepareStatement(
						"INSERT INTO JOUEUR VALUES(?,?,?,?)"
						);
				statement.setInt(1, idMap);
				statement.setInt(2, DTO.getJoueurs()[i].getX());
				statement.setInt(3, DTO.getJoueurs()[i].getY());			
				statement.setInt(4, i+1);
				
				executeStatement(statement);
			} catch (SQLException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
				return false;
			}
		}
		
		// s'il n'y a eu aucune erreur
		return true;
	}
}



