package Projet;

import java.awt.BorderLayout;
import javax.swing.JOptionPane;
import java.awt.Color;
import java.awt.EventQueue;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.event.MouseMotionListener;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.border.EmptyBorder;

import javax.swing.ImageIcon;
import javax.swing.JButton;

import java.util.Vector;
import javax.swing.JTextField;
import javax.swing.TransferHandler;
import javax.swing.JLabel;
import java.awt.Font;
import javax.swing.JSpinner;
import javax.swing.JList;
import javax.swing.JComboBox;
import javax.swing.JComponent;
import javax.swing.border.CompoundBorder;
import javax.swing.border.LineBorder;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;

import java.awt.GridLayout;
import javax.swing.SpinnerNumberModel;

public class Editeur extends JFrame {
	private EcouteurBoutons ecouteurBoutons;
	private EcouteurCanvas ecouteurCanvas;
	private Vector<Element> elements;
	private String selection;
	private int cols = 12;
	private int tempc;
	private int rows = 12;
	private int tempr;
	private Dessin dessin;
	private Case[][] cases;
	private JPanel contentPane;
	private int taille = 750;
	private int tailleDeLaCase;
	private Color couleurElement;
	private JTextField textfield_titre_map;
	private Boolean arbre_selectionne = false;
	private JComboBox combobox_joueur;
	private JSpinner spinner_mapy;
	private JSpinner spinner_mapx;
	JLabel lblStatutDuNiveau;
	JLabel invisible_label;
	private Boolean deplacer_joueur = false;
	private Boolean placer_joueur1 = false;
	private Boolean efface = false;
	private int mapy;
	private int mapx;
	private String type_element; 
	private JButton effacer_arbre;
	private JButton resize;
	private Boolean placer_joueur2 = false;
	private Boolean enlever_arbre = false;
	private JComboBox combobox_statut_niveau;
	private JTextField txt_elementSelectionne;
	private Joueur joueur_1; 
	private Joueur joueur_2; 
	private JSpinner spinner_delai_objets_min;
	private JSpinner spinner_delai_objets_max;
	private JButton btnNewButton;
private Color couleurMap = new Color (51,102,0);	private Joueur[] joueurs;
	

	
	
	/**
	 * Launch the application.
	 */
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					
					Editeur frame = new Editeur();
					frame.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}

	/**
	 * Create the frame.
	 * @throws IOException 
	 */
	
	public Editeur() throws IOException {
		setTitle("TANKEM        Editeur de niveau ");
		setResizable(false);
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(100, 100, 1200, 900);
		contentPane = new JPanel();
		contentPane.setBorder(new EmptyBorder(5, 5, 5, 5));
		setContentPane(contentPane);
		contentPane.setLayout(null);
		  

		// ajouter les joueurs
		joueurs = new Joueur[]{new Joueur(), new Joueur()};
		joueurs[0].setX(0);
		joueurs[0].setY(0);
		joueurs[1].setX(0);
		joueurs[1].setY(1);
				
		
	
		// cr�er les cases
		cases =  new Case[cols][rows];
		
		if (cols > rows)
		{
			tailleDeLaCase = taille / cols;
		}
		else
		{
			tailleDeLaCase = taille / rows;
		}

		/*Map couleur*/
		for (int col = 0; col < cols; col++)
		{
			for (int row = 0; row < rows; row++)
			{
				cases[col][row] = (new Case(col,row,tailleDeLaCase,"plancher"));
				
				
			}
		}
		
		
		cases[0][0].setJoueur1(true);
		cases[0][1].setJoueur2(true);
		
		
		
		
		
		
		ecouteurCanvas = new EcouteurCanvas();
		dessin = new Dessin();
		dessin.addMouseListener(ecouteurCanvas);
		
		dessin.setBounds(400,50, taille, taille);
		dessin.setLayout(null);
		getContentPane().add(dessin);
		

	
		
		
	
		
		//Mettre le text dans le label
		String ligne = Integer.toString(cols); 
		//valx.setText(ligne);
		String coll = Integer.toString(rows); 
		//valy.setText(coll);
		
		JButton btnSauvegarde = new JButton("Enregistrer");
		btnSauvegarde.setFont(new Font("Tahoma", Font.PLAIN, 12));
		btnSauvegarde.setBounds(1042,813, 112, 33);
		contentPane.add(btnSauvegarde);
		
		
	
		textfield_titre_map = new JTextField();
		textfield_titre_map.setBounds(463, 11, 691, 20);
		contentPane.add(textfield_titre_map);
		textfield_titre_map.setColumns(10);
		
		JLabel lblTitre = new JLabel("Titre :");
		lblTitre.setFont(new Font("Tahoma", Font.PLAIN, 16));
		lblTitre.setBounds(405, 12, 48, 14);
		contentPane.add(lblTitre);
		
		JPanel panel = new JPanel();
		panel.setBorder(new LineBorder(new Color(0, 0, 0), 1, true));
		panel.setBounds(10, 59, 381, 249);
		contentPane.add(panel);
		panel.setLayout(null);
		
		JLabel lblNewLabel = new JLabel("Taille de la map :");
		lblNewLabel.setBounds(20, 11, 92, 15);
		panel.add(lblNewLabel);
		lblNewLabel.setFont(new Font("Tahoma", Font.PLAIN, 12));
		
		JLabel lblX_1 = new JLabel("X :");
		lblX_1.setBounds(37, 37, 21, 14);
		panel.add(lblX_1);
		
		spinner_mapx = new JSpinner();
		spinner_mapx.setModel(new SpinnerNumberModel(12, 6, 12, 1));
		spinner_mapx.setBounds(64, 32, 48, 19);
		panel.add(spinner_mapx);
		
		
		
		JLabel lblY_1 = new JLabel("Y :");
		lblY_1.setBounds(37, 65, 23, 19);
		panel.add(lblY_1);
		
		spinner_mapy = new JSpinner();
		spinner_mapy.setModel(new SpinnerNumberModel(12, 6, 12, 1));
		spinner_mapy.setBounds(64, 62, 48, 22);
		panel.add(spinner_mapy);
		
	
		resize = new JButton("Redimensionner");
		resize.setBounds(130, 48, 120, 23);
		panel.add(resize);
		resize.setFont(new Font("Tahoma", Font.PLAIN, 12));
		
		 lblStatutDuNiveau = new JLabel("Statut du niveau :");
		lblStatutDuNiveau.setBounds(20, 95, 165, 14);
		panel.add(lblStatutDuNiveau);
		
		String[] Statut = {"Actif","Inactif","Test"};
		
		combobox_statut_niveau = new JComboBox(Statut);
		combobox_statut_niveau.setBounds(20, 120, 230, 20);
		panel.add(combobox_statut_niveau);
		
		JLabel lblDlaisDapparitionDes = new JLabel("Délais d'apparition des objets :");
		lblDlaisDapparitionDes.setBounds(20, 160, 230, 14);
		panel.add(lblDlaisDapparitionDes);
		
		JLabel lblMin = new JLabel("min : ");
		lblMin.setBounds(30, 185, 41, 14);
		panel.add(lblMin);
		
		spinner_delai_objets_min = new JSpinner();
		spinner_delai_objets_min.setBounds(64, 182, 41, 20);
		panel.add(spinner_delai_objets_min);
		
		JLabel lblMax = new JLabel("max : ");
		lblMax.setBounds(139, 185, 46, 14);
		panel.add(lblMax);
		
		spinner_delai_objets_max = new JSpinner();
		spinner_delai_objets_max.setBounds(172, 182, 41, 20);
		panel.add(spinner_delai_objets_max);
	
		JPanel panel_1 = new JPanel();
		panel_1.setBorder(new LineBorder(new Color(0, 0, 0), 1, true));
		panel_1.setBounds(10, 319, 381, 483);
		contentPane.add(panel_1);
		panel_1.setLayout(null);
		
		JLabel lblUneFoisLlment = new JLabel("INSTRUCTION : Une fois l'élément sélectionné, cliquez");
		lblUneFoisLlment.setBounds(10, 23, 335, 14);
		panel_1.add(lblUneFoisLlment);
		
		JLabel lblPourLePlacer = new JLabel("sur la map pour le placer. ");
		lblPourLePlacer.setBounds(10, 38, 164, 14);
		panel_1.add(lblPourLePlacer);
		
		JPanel panel_boutons = new JPanel();
		panel_boutons.setBounds(10, 119, 262, 353);
		panel_1.add(panel_boutons);
		panel_boutons.setLayout(new GridLayout(0, 1, 0, 0));
		
		JLabel lblNewLabel_1 = new JLabel("Position");
		lblNewLabel_1.setBounds(10, 79, 46, 14);
		panel_1.add(lblNewLabel_1);
		
		
		String[] Joueurs = {"Sélectionnez un joueur","Joueur 1","Joueur 2"};
		
		combobox_joueur = new JComboBox(Joueurs);
		combobox_joueur.setBounds(64, 76, 208, 20);
		panel_1.add(combobox_joueur);
		
		resize.addActionListener(ecouteurCanvas);
		
		ecouteurBoutons = new EcouteurBoutons();
		elements = new Vector<Element>();
		elements.add(new Element(Color.ORANGE,"Arbre","arbre"));
		elements.add(new Element(new Color(51,255,51),"Mur animé","murAnime"));
		elements.add(new Element(new Color(230, 204, 255),"Mur animé inverse","murAnimeInverse"));
		elements.add(new Element(new Color(73,153,0),"Mur fixe","murFixe"));
		elements.add(new Element(new Color(51,102,0),"Plancher","plancher"));
		
		
		//cols = tempc;
		//rows = tempr; 
	
		for (int i = 0; i < elements.size(); i++)
		{
			JButton nouveauBouton = new JButton(elements.elementAt(i).nom());
			nouveauBouton.setBounds(30, 86 + i * 80, 194, 55);
			panel_boutons.add(nouveauBouton);
			nouveauBouton.addMouseListener(ecouteurBoutons);
			elements.elementAt(i).setBouton(nouveauBouton);
		}
		
		JButton btnJoueur = new JButton("Placer Joueur");
		btnJoueur.setBounds(282, 75, 89, 23);
		panel_1.add(btnJoueur);
		btnJoueur.addMouseListener(ecouteurBoutons);
		
		JLabel lblPourPlacerUn = new JLabel("Pour placer un Joueur, cliquez sur \"placer joueur\".");
		lblPourPlacerUn.setBounds(10, 54, 327, 14);
		panel_1.add(lblPourPlacerUn);
		
		JLabel tag_arbre = new JLabel(" A");
		tag_arbre.setOpaque(true);
		tag_arbre.setBackground(new Color(51,102,0));
		tag_arbre.setFont(new Font("Tahoma", Font.PLAIN, 30));
		tag_arbre.setForeground(Color.ORANGE);
		tag_arbre.setBounds(291, 139, 46, 42);
		panel_1.add(tag_arbre);
		
		JLabel tag_murFixe = new JLabel("");
		tag_murFixe.setBackground(new Color(73,153,0));
		tag_murFixe.setOpaque(true);
		tag_murFixe.setBounds(291, 340, 46, 42);
		panel_1.add(tag_murFixe);
		
		JLabel tag_murAnime = new JLabel("");
		tag_murAnime.setOpaque(true);
		tag_murAnime.setBackground(new Color(51,255,51));
		tag_murAnime.setBounds(291, 206, 46, 42);
		panel_1.add(tag_murAnime);
		
		JLabel tag_murInverse = new JLabel("");
		tag_murInverse.setOpaque(true);
		tag_murInverse.setBackground(new Color(230, 204, 255));
		tag_murInverse.setBounds(291, 272, 46, 42);
		panel_1.add(tag_murInverse);
		
		JLabel tag_plancher = new JLabel("");
		tag_plancher.setOpaque(true);
		tag_plancher.setBackground(new Color(51,102,0));
		tag_plancher.setBounds(291, 413, 46, 42);
		panel_1.add(tag_plancher);

		btnJoueur.addMouseListener(ecouteurBoutons);
		spinner_mapx.addChangeListener(ecouteurCanvas);
		spinner_mapy.addChangeListener(ecouteurCanvas);

		
		JButton effacer_arbre = new JButton("Effacer un arbre");
		effacer_arbre.setBounds(692, 814, 162, 33);
		
		effacer_arbre.addMouseListener(ecouteurBoutons);
		contentPane.add(effacer_arbre);
		
		btnSauvegarde.addMouseListener(ecouteurBoutons);
		JLabel lbllementSlectionn = new JLabel("\u00C9lement S\u00E9lectionn\u00E9 :");
		lbllementSlectionn.setForeground(new Color(0, 0, 255));
		lbllementSlectionn.setFont(new Font("Tahoma", Font.PLAIN, 15));
		lbllementSlectionn.setBounds(10, 34, 176, 14);
		contentPane.add(lbllementSlectionn);
		
		txt_elementSelectionne = new JTextField();
		txt_elementSelectionne.setForeground(new Color(255, 0, 0));
		txt_elementSelectionne.setBounds(159, 33, 232, 20);
		contentPane.add(txt_elementSelectionne);
		txt_elementSelectionne.setColumns(10);		
		
	
		btnNewButton = new JButton("Effacer tout");
		btnNewButton.setBounds(911, 813, 107, 33);
		contentPane.add(btnNewButton);
		btnNewButton.setFont(new Font("Tahoma", Font.PLAIN, 12));
		
			btnNewButton.addActionListener(ecouteurCanvas);
		
		
	}
	
	
	public void set_tag(String type_element) {
		if(type_element!= null) {
		if(type_element.equals("murAnime")) {
			txt_elementSelectionne.setText("Mur anim�");
		}
		if(type_element.equals("murAnimeInverse")) {
			txt_elementSelectionne.setText("Mur anim� inverse");
		}
		if(type_element.equals("murFixe")) {
			txt_elementSelectionne.setText("Mur fixe");
		}
		if(type_element.equals("plancher")) {
			txt_elementSelectionne.setText("Plancher");
		}
		}
	}
	
	private class Dessin extends JPanel
	{
		protected void paintComponent(Graphics g)
		{
			super.paintComponent(g);
			this.setBackground(new Color(51,102,0));
			this.setOpaque(true);
			this.setVisible(true);
			Graphics2D g2 = (Graphics2D) g;

			
			
			
			
			
			for (int col = 0; col < cols; col++)
			{
				for (int row = 0; row < rows; row++)
				{
					cases[col][row].dessiner(g);
					if(cases[col][row].withArbre()) {
						cases[col][row].dessiner_arbre(g);
						
					}
					
					
					
					if(cases[col][row].joueur_1_actif()) {
						cases[col][row].dessiner_joueur(g, "J1");
					}
					
					if(cases[col][row].joueur_2_actif()) {
						cases[col][row].dessiner_joueur(g, "J2");
					}
				}
			
		
			}
			
			cases[0][0].dessiner_caseRouge(g);
			
			if (efface == true)
			{
				for (int col = 0; col < cols; col++)
				{
					for (int row = 0; row < rows; row++)
					{
							cases[col][row].dessiner(g);
							if(cases[col][row].withArbre())
							{
								cases[col][row].setArbre(false);
								
							}
							
						
					}
				}
				
			}
		
		

		}
	}
	

	
	private class EcouteurCanvas implements MouseListener, ActionListener, ChangeListener
	{
		@Override
		public void mouseClicked(MouseEvent b) {
			int x = b.getX();
			int y = b.getY();
			int col = (int)(x / tailleDeLaCase);
			int row = (int)(y / tailleDeLaCase);
			
			
			if(placer_joueur1)
			{
				
				placer_joueur2=false;
				for(int i = 0 ; i < cols ; ++i) {
					for(int j = 0; j <rows ; ++j) {
						cases[i][j].setJoueur1(false);
					}}
				if(cases[col][row].withArbre() == false) {
				cases[col][row].setJoueur1(true);
				joueurs[0].setX(col);
				joueurs[0].setY(row);
				placer_joueur1=false;
				set_tag(type_element);
				
				}
			}
			
			if(placer_joueur2) {
				placer_joueur1=false;
				for(int l = 0 ; l < cols ; ++l)
				{
					for(int m = 0; m <rows ; ++m) {
						cases[l][m].setJoueur2(false);	
					}
					
					}
				
				if(cases[col][row].withArbre() == false) {
				cases[col][row].setJoueur2(true);

				joueurs[1].setX(col);
				joueurs[1].setY(row);
				}
				placer_joueur2 = false;
				set_tag(type_element);
				}
				
					
				
			efface = false;
			if(arbre_selectionne) {
				
				if(!cases[col][row].joueur_1_actif() && !cases[col][row].joueur_2_actif()) {
					cases[col][row].setArbre(true);
					arbre_selectionne = false;
					
					}
				set_tag(type_element);	
			}
			if(enlever_arbre){
				if(cases[col][row].withArbre()){
					cases[col][row].setArbre(false);
				}
				enlever_arbre = false;
			}
	
			efface = false;
			if (col < cols && row < rows)
			{
				
				cases[col][row].setColor(couleurElement); 
				cases[col][row].setType(type_element);
				
				
			}
	
			
			
			
			repaint();
			}
			
		
			
				
		

		@Override
		public void mouseEntered(MouseEvent ee) {
			// TODO Auto-generated method stub
			
			
			
		}

		@Override
		public void mouseExited(MouseEvent arg0) {
			// TODO Auto-generated method stub
			
		}

		@Override
		public void mousePressed(MouseEvent arg0) {
			// TODO Auto-generated method stub
			
		}

		@Override
		public void mouseReleased(MouseEvent arg0) {
			// TODO Auto-generated method stub
			
		}

		//Pour faire changer le map selon coordonn�es
		@Override
		public void actionPerformed(ActionEvent e) {
			
			
			if(e.getSource() == resize)
			{
			
			
				rows = mapx;
				cols = mapy;
				repaint();
			}
			
			
			if (e.getSource() == btnNewButton)
			{
				efface = true;
				
				
				
				
				
				
					
					for (int col = 0; col < cols; col++)
					{
						for (int row = 0; row < rows; row++)
						{
							int rowCorrection = rows-row-1;
							cases[col][row] = (new Case(col,rowCorrection,tailleDeLaCase,"plancher"));
						}
					}
					
				repaint();
				
			}
			else
			{
				efface= false;
			}
			
			
		}


		@Override
		public void stateChanged(ChangeEvent e) {
			// TODO Auto-generated method stub
			
		
			
			 mapx =(Integer) spinner_mapx.getValue();
			 mapy =(Integer) spinner_mapy.getValue();
			
			
			
			
			
		}


	}
	
	

	private class EcouteurBoutons implements MouseListener
	{
		@Override
		public void mouseClicked(MouseEvent b) {
			JButton bouton = (JButton)b.getSource();
			// TODO Auto-generated method stub
			
			
			
			
			if(bouton.getText().equals("Effacer un arbre")){
				enlever_arbre = true;
			}
			if(bouton.getText().equals("Placer Joueur")) {
				
				
				if(combobox_joueur.getSelectedItem().equals("Joueur 1")) {
					placer_joueur1 = true;
					txt_elementSelectionne.setText("Joueur 1");
				}
				if(combobox_joueur.getSelectedItem().equals("Joueur 2")) {
					placer_joueur2 = true;
					txt_elementSelectionne.setText("Joueur 2");
				}
				
			}
			
			
			if (bouton.getText().equals("Arbre")) {
				arbre_selectionne = true;
				txt_elementSelectionne.setText("Arbre");
			}
			else {
				
				arbre_selectionne = false;
			
			
				/*Selon le bouton choisi, ajoute dans le dessin*/
			for (int i =0; i < elements.size(); i++)
			{
				Element element = elements.elementAt(i);
				if (bouton == element.bouton())
				{	
					selection = element.nom();
					couleurElement = element.couleur();
					type_element = element.getType();
					break;
					
					
				
				
				}		
			}
			
			
			// Permet d'afficher le type de mur s�lectionn� dans le champs "�l�ment s�lectionn�"
			
			if(txt_elementSelectionne.getText().equals("Joueur 1") || txt_elementSelectionne.getText().equals("Joueur 2")) {
		
			
			}
			else {
				set_tag(type_element);
				
			}
			
			
			
			
			}
			
			

			if (bouton.getText().equals("Enregistrer"))
			{
				
				// remplissage du DTO
				
				DTO.setTitre(textfield_titre_map.getText());
				DTO.setNbColonne((Integer)spinner_mapx.getValue());
				DTO.setNbLigne((Integer)spinner_mapy.getValue());
				DTO.setStatut(combobox_statut_niveau.getSelectedItem().toString());
				DTO.setCases(cases);
				DTO.setJoueurs(joueurs);
				DTO.setDelaiApparitionMin((Integer)spinner_delai_objets_min.getValue());
				DTO.setDelaiApparitionMax((Integer)spinner_delai_objets_max.getValue());

				// �criture dans la BD
				DAO_Oracle dao = new DAO_Oracle();
				dao.connexion();
				boolean success = dao.insertionDansLaBD();				
				dao.deconnexion();
				
				if (success)
				{
					JOptionPane.showMessageDialog(null, "L'insertion a ete faite!", "Reussite",
	                        JOptionPane.PLAIN_MESSAGE);
				}
				else
				{
					JOptionPane.showMessageDialog(null, "Des erreurs d'insertion ont eu lieu", "Echec",
	                        JOptionPane.ERROR_MESSAGE);
				}


			}
		}

		@Override
		public void mouseEntered(MouseEvent arg0) {
			// TODO Auto-generated method stub
			
		}

		@Override
		public void mouseExited(MouseEvent arg0) {
			// TODO Auto-generated method stub
			
		}

		@Override
		public void mousePressed(MouseEvent arg0) {
			// TODO Auto-generated method stub
			  
		}
		

		@Override
		public void mouseReleased(MouseEvent arg0) {
			// TODO Auto-generated method stub
			
		}
		
	}
}