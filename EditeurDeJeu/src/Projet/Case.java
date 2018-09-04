package Projet;

import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Image;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.net.URL;

import javax.imageio.ImageIO;
import javax.swing.ImageIcon;

public class Case {
	
	private int mCol;	
	private int mRow;
	private int mTaille;
	private Color mColor = null;
	private Boolean arbre_selectionne = false;
	private String type; // mur, plancher etc 
	private Boolean Joueur_1_status = false;
	private Boolean Joueur_2_status = false;
	private BufferedImage image ;


	
	Case(int col, int row, int taille, String type) 
	{
		this.mCol = col;
		this.mRow = row;
		this.mTaille = taille;
		this.type = type;
	}
	
	public void dessiner(Graphics g)
	{
		g.setColor(this.mColor);
		Graphics2D g2 = (Graphics2D) g;
		if (this.mColor == null)
		{
			g.setColor(Color.orange);
			g.drawRect(this.mCol * this.mTaille,this.mRow * this.mTaille, this.mTaille, this.mTaille);
		}
		else
		{	
			
			g.setColor(this.mColor);
			g.fillRect(this.mCol * this.mTaille,this.mRow * this.mTaille, this.mTaille, this.mTaille);
			g.setColor(Color.orange);
			g.drawRect(this.mCol * this.mTaille,this.mRow * this.mTaille, this.mTaille, this.mTaille);
		}
		
	}
	
	public void dessiner_caseRouge(Graphics g) {
		Graphics2D g2 = (Graphics2D) g;
		g.setColor(Color.red);
		g.drawRect(this.mCol * this.mTaille,this.mRow * this.mTaille, this.mTaille, this.mTaille);
	}
	
	public Boolean joueur_1_actif() {
		return Joueur_1_status;
	}
	
	public Boolean joueur_2_actif() {
		return Joueur_2_status;
	}
	
	public void setJoueur1(Boolean statut) {
		Joueur_1_status = statut;
	}
	
	public void setJoueur2(Boolean statut) {
		Joueur_2_status = statut;
	}
	
	public Boolean withArbre() {
		return arbre_selectionne;
	}
	public void setArbre(Boolean status) {
		arbre_selectionne = status;
	}
	
	
	public void dessiner_joueur(Graphics g, String joueur) {
		Font stringFont = new Font( "SansSerif", Font.PLAIN, 40 );
		g.setFont(stringFont);
		if(joueur.equals("J1")) {
		g.setColor(Color.PINK);}
		if(joueur.equals("J2")) {
			g.setColor(Color.MAGENTA);}
		Graphics2D g2 = (Graphics2D) g;
		g.drawString(joueur,this.mCol * this.mTaille ,(this.mRow + 1 ) * this.mTaille);
	}
	public void dessiner_arbre(Graphics g) {
		g.setColor(new Color(255,121,0));
		Graphics2D g2 = (Graphics2D) g;
		Font stringFont = new Font( "SansSerif", Font.PLAIN, 40 );
		g.setFont(stringFont);
		g.drawString("A",this.mCol * this.mTaille ,(this.mRow + 1 ) * this.mTaille);
	}
	
	public void setColor(Color color)
	{
		this.mColor = color;
	}

	public String getType() {
		return type;
	}

	public void setType(String type) {
		this.type = type;
	}
	
	// accesseurs
	public int getCol()
	{
		return this.mCol;
	}
	
	public int getRow()
	{
		return this.mRow;
	}
}
