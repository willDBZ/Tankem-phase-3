package Projet;

import java.awt.Color;

import javax.swing.JButton;

public class Element {
	//variable statique
	public static int sIdGeneral = 0;
	
	//variables membres
	private Color mCouleur;
	private JButton mBouton;
	private String mNom;
	private int mId;
	private String type;
	
	Element(Color couleur, String nom, String type)
	{
		this.mNom = nom;
		this.mCouleur = couleur;
		this.mId = sIdGeneral;
		this.setType(type);
		sIdGeneral++;
	}
	
	//accesseurs
	Color couleur()
	{
		return this.mCouleur;
	}
	
	JButton bouton()
	{
		return this.mBouton;
	}
	
	String nom()
	{
		return this.mNom;
	}
	
	//modificateur(s)
	void setBouton(JButton bouton)
	{
		this.mBouton = bouton;
	}

	public String getType() {
		return type;
	}

	public void setType(String type) {
		this.type = type;
	}
	
	
}
