package Projet;

public class DTO {
	/*
	 * static private Joueur[] joueurs; static private Case[][] cases; static
	 * private int nbColonne; static private int nbLigne; static private String
	 * statut; static private float delaiApparitionMax; static private float
	 * delaiApparitionMin; static private String titre;
	 */

	static private Joueur[] joueurs;
	static private Case[][] cases;
	static private int nbColonne = 6;
	static private int nbLigne = 6;
	static private String statut = "Actif";
	static private double delaiApparitionMax = 0.2;
	static private double delaiApparitionMin = 0.5;
	static private String titre = "hey";

	public static String getTitre() {
		return titre;
	}

	public static Joueur[] getJoueurs() {

		return joueurs;
	}

	public static Case[][] getCases() {
		return cases;
	}

	public static int getNbColonne() {
		return nbColonne;
	}

	public static int getNbLigne() {
		return nbLigne;
	}

	public static String getStatut() {
		return statut;
	}

	public static double getDelaiApparitionMax() {
		return delaiApparitionMax;
	}

	public static double getDelaiApparitionMin() {
		return delaiApparitionMin;
	}

	/* mes setteurs */

	public static void setTitre(String pTitre) {
		titre = pTitre;
	}

	public static void setJoueurs(Joueur[] pJoueurs) {
		joueurs = pJoueurs;
	}

	public static void setCases(Case[][] pCases) {
		cases = pCases;
	}

	public static void setNbColonne(int pNbColonne) {
		nbColonne = pNbColonne;
	}

	public static void setNbLigne(int pNbLigne) {
		nbLigne = pNbLigne;
	}

	public static void setStatut(String pStatut) {
		statut = pStatut;
	}

	public static void setDelaiApparitionMax(int pDelaiApparitionMax) {
		delaiApparitionMax = pDelaiApparitionMax;
	}

	public static void setDelaiApparitionMin(int pDelaiApparitionMin) {
		delaiApparitionMin = pDelaiApparitionMin;
	}
}
