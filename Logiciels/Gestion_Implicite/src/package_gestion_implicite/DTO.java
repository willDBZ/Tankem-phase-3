package package_gestion_implicite;
import java.util.Vector;

public class DTO {
	/*Classe conteneur*/

	private String nom_du_joueur;
	private int experience;
	private int coolpoints_vie;
	private int coolpoints_force;
	private int coolpoints_agilite;
	private int coolpoints_dexterite;
	
	private String phrase_du_joueur;
	
	private int couleur_tank_rouge;
	private int couleur_tank_vert;
	private int couleur_tank_bleu;
	
	private Vector<String> armes_joueur;
	private Vector<String> dates_des_parties_jouees;
	private String arme_prefere;  // a déterminer avec une requête dans le DAO 
	private String arme_efficace; // a déterminer avec une requête dans le DAO 
	
	private int total_parties_jouees;
	private int total_parties_gagnees;
	private int total_parties_perdues;
	
	
	public String getNom_du_joueur() {
		return nom_du_joueur;
	}
	public void setNom_du_joueur(String nom_du_joueur) {
		this.nom_du_joueur = nom_du_joueur;
	}
	public int getCoolpoints_vie() {
		return coolpoints_vie;
	}
	public void setCoolpoints_vie(int coolpoints_vie) {
		this.coolpoints_vie = coolpoints_vie;
	}
	public int getCoolpoints_force() {
		return coolpoints_force;
	}
	public void setCoolpoints_force(int coolpoints_force) {
		this.coolpoints_force = coolpoints_force;
	}
	public int getCoolpoints_agilite() {
		return coolpoints_agilite;
	}
	public void setCoolpoints_agilite(int coolpoints_agilite) {
		this.coolpoints_agilite = coolpoints_agilite;
	}
	public int getCoolpoints_dexterite() {
		return coolpoints_dexterite;
	}
	public void setCoolpoints_dexterite(int coolpoints_dexterite) {
		this.coolpoints_dexterite = coolpoints_dexterite;
	}
	public String getPhrase_du_joueur() {
		return phrase_du_joueur;
	}
	public void setPhrase_du_joueur(String phrase_du_joueur) {
		this.phrase_du_joueur = phrase_du_joueur;
	}

	public int getCouleur_tank_rouge() {
		return couleur_tank_rouge;
	}
	public void setCouleur_tank_rouge(int couleur_tank_rouge) {
		this.couleur_tank_rouge = couleur_tank_rouge;
	}
	public int getCouleur_tank_vert() {
		return couleur_tank_vert;
	}
	public void setCouleur_tank_vert(int couleur_tank_vert) {
		this.couleur_tank_vert = couleur_tank_vert;
	}
	public int getCouleur_tank_bleu() {
		return couleur_tank_bleu;
	}
	public void setCouleur_tank_bleu(int couleur_tank_bleu) {
		this.couleur_tank_bleu = couleur_tank_bleu;
	}
	public Vector<String> getArmes_joueur() {
		return armes_joueur;
	}
	public void setArmes_joueur(Vector<String> armes_joueur) {
		this.armes_joueur = armes_joueur;
	}
	public String getArme_prefere() {
		return arme_prefere;
	}
	public void setArme_prefere(String arme_prefere) {
		this.arme_prefere = arme_prefere;
	}
	public String getArme_efficace() {
		return arme_efficace;
	}
	public void setArme_efficace(String arme_efficace) {
		this.arme_efficace = arme_efficace;
	}
	public int getTotal_parties_jouees() {
		return total_parties_jouees;
	}
	public void setTotal_parties_jouees(int total_parties_jouees) {
		this.total_parties_jouees = total_parties_jouees;
	}
	public int getTotal_parties_gagnees() {
		return total_parties_gagnees;
	}
	public void setTotal_parties_gagnees(int total_parties_gagnees) {
		this.total_parties_gagnees = total_parties_gagnees;
	}
	public int getTotal_parties_perdues() {
		return total_parties_perdues;
	}
	public void setTotal_parties_perdues(int total_parties_perdues) {
		this.total_parties_perdues = total_parties_perdues;
	}
	public int getExperience() {
		return experience;
	}
	public void setExperience(int experience) {
		this.experience = experience;
	}
	
	//La densité de partie jouées dans le temps. 
	
	
	
}
