package package_gestion_implicite;
import java.awt.EventQueue;

import javax.swing.JComponent;
import javax.swing.JFrame;
import javax.swing.JTabbedPane;
import javax.swing.JPanel;
import javax.swing.JLabel;
import javax.swing.SwingConstants;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;

import java.awt.Font;
import java.awt.FlowLayout;
import java.awt.BorderLayout;
import javax.swing.JSpinner;
import javax.swing.JComboBox;
import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.data.general.DefaultPieDataset;
import org.jfree.data.general.PieDataset;
import org.jfree.ui.ApplicationFrame;
import org.jfree.ui.RefineryUtilities;


public class ParametreUtilisateur extends JFrame {
	JTabbedPane tabbedPane;
	private Ecouteur ec;
	private Joueur joueur;
	private GestionCoolPoints gestioncp;
	private Statistiques statist;
	/**
	 * Launch the application.
	 */
	
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					ParametreUtilisateur frame = new ParametreUtilisateur();
					frame.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}
	

	/**
	 * Create the frame.
	 */
	public ParametreUtilisateur() {
		setBounds(100, 100, 734, 449);
		setTitle("Parametre du Joueur");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		getContentPane().setLayout(new BorderLayout(0, 0));
		
		JTabbedPane tab_Param_Joueur = new JTabbedPane(JTabbedPane.TOP);
		getContentPane().add(tab_Param_Joueur, BorderLayout.CENTER);
		
		JPanel panel_Joueur = new JPanel();
		tab_Param_Joueur.addTab("Joueur", null, panel_Joueur, null);
		panel_Joueur.setLayout(null);
		
		JLabel lblPhrase = new JLabel("Phrase Personnelle");
		lblPhrase.setHorizontalAlignment(SwingConstants.CENTER);
		lblPhrase.setFont(new Font("Dialog", Font.PLAIN, 14));
		lblPhrase.setBounds(242, 73, 191, 14);
		panel_Joueur.add(lblPhrase);
		
		JLabel LblNom = new JLabel("Nom du Joueur");
		LblNom.setHorizontalAlignment(SwingConstants.CENTER);
		LblNom.setFont(new Font("Dialog", Font.PLAIN, 14));
		LblNom.setBounds(230, 11, 191, 14);
		panel_Joueur.add(LblNom);
		
		JLabel lblXP = new JLabel("XP:");
		lblXP.setHorizontalAlignment(SwingConstants.CENTER);
		lblXP.setFont(new Font("Dialog", Font.PLAIN, 14));
		lblXP.setBounds(242, 180, 191, 14);
		panel_Joueur.add(lblXP);
		
		JLabel lblNiveau = new JLabel("Niveau:");
		lblNiveau.setHorizontalAlignment(SwingConstants.CENTER);
		lblNiveau.setFont(new Font("Dialog", Font.PLAIN, 14));
		lblNiveau.setBounds(242, 252, 191, 14);
		panel_Joueur.add(lblNiveau);
		
		JLabel lblDateDernierePartie = new JLabel("Date Derniere Partie:");
		lblDateDernierePartie.setHorizontalAlignment(SwingConstants.CENTER);
		lblDateDernierePartie.setFont(new Font("Dialog", Font.PLAIN, 14));
		lblDateDernierePartie.setBounds(242, 313, 191, 14);
		panel_Joueur.add(lblDateDernierePartie);
		
		JLabel lblNomJoueur = new JLabel("New label");
		lblNomJoueur.setBounds(304, 36, 81, 14);
		panel_Joueur.add(lblNomJoueur);
		
		JLabel lblPhraseJoueur = new JLabel("New label");
		lblPhraseJoueur.setBounds(304, 98, 67, 14);
		panel_Joueur.add(lblPhraseJoueur);
		
		JLabel lblXPJoueur = new JLabel("0000000000");
		lblXPJoueur.setBounds(304, 205, 81, 14);
		panel_Joueur.add(lblXPJoueur);
		
		JLabel lblNiveauJoueur = new JLabel("0");
		lblNiveauJoueur.setBounds(332, 277, 24, 14);
		panel_Joueur.add(lblNiveauJoueur);
		
		JLabel lblDateJoueur = new JLabel("New label");
		lblDateJoueur.setBounds(304, 338, 81, 14);
		panel_Joueur.add(lblDateJoueur);
		
		JLabel lblCouleurDuTank = new JLabel("Couleur du Tank :");
		lblCouleurDuTank.setFont(new Font("Dialog", Font.PLAIN, 14));
		lblCouleurDuTank.setBounds(132, 137, 114, 14);
		panel_Joueur.add(lblCouleurDuTank);
		
		JComboBox comboBox = new JComboBox();
		comboBox.setBounds(256, 136, 167, 20);
		panel_Joueur.add(comboBox);
		
		JPanel panel_CoolPoint = new JPanel();
		tab_Param_Joueur.addTab("Cool Points", null, panel_CoolPoint, null);
		panel_CoolPoint.setLayout(null);
		
		JLabel lblCoolPoints = new JLabel("CoolPoint Disponible");
		lblCoolPoints.setHorizontalAlignment(SwingConstants.LEFT);
		lblCoolPoints.setFont(new Font("Dialog", Font.PLAIN, 15));
		lblCoolPoints.setBounds(224, 21, 191, 14);
		panel_CoolPoint.add(lblCoolPoints);
		
		JLabel lblVie = new JLabel("Vie:");
		lblVie.setHorizontalAlignment(SwingConstants.CENTER);
		lblVie.setFont(new Font("Dialog", Font.PLAIN, 15));
		lblVie.setBounds(42, 103, 191, 14);
		panel_CoolPoint.add(lblVie);
		
		JLabel lblForce = new JLabel("Force:");
		lblForce.setHorizontalAlignment(SwingConstants.CENTER);
		lblForce.setFont(new Font("Dialog", Font.PLAIN, 15));
		lblForce.setBounds(42, 153, 191, 14);
		panel_CoolPoint.add(lblForce);
		
		JLabel lblAgilite = new JLabel("Agilite:");
		lblAgilite.setHorizontalAlignment(SwingConstants.CENTER);
		lblAgilite.setFont(new Font("Dialog", Font.PLAIN, 15));
		lblAgilite.setBounds(42, 199, 191, 14);
		panel_CoolPoint.add(lblAgilite);
		
		JLabel lblDexterite = new JLabel("Dexterite:");
		lblDexterite.setHorizontalAlignment(SwingConstants.CENTER);
		lblDexterite.setFont(new Font("Dialog", Font.PLAIN, 15));
		lblDexterite.setBounds(42, 240, 191, 14);
		panel_CoolPoint.add(lblDexterite);
		
		JSpinner spinVie = new JSpinner();
		spinVie.setBounds(224, 102, 29, 20);
		panel_CoolPoint.add(spinVie);
		
		JSpinner spinForce = new JSpinner();
		spinForce.setBounds(224, 152, 29, 20);
		panel_CoolPoint.add(spinForce);
		
		JSpinner spinAgilite = new JSpinner();
		spinAgilite.setBounds(224, 198, 29, 20);
		panel_CoolPoint.add(spinAgilite);
		
		JSpinner spinDext = new JSpinner();
		spinDext.setBounds(224, 239, 29, 20);
		panel_CoolPoint.add(spinDext);
		
		JLabel lblPointJoueur = new JLabel("New label");
		lblPointJoueur.setBounds(142, 23, 72, 14);
		panel_CoolPoint.add(lblPointJoueur);
		
		JPanel panel_Stat = new JPanel();
		tab_Param_Joueur.addTab("Statistique", null, panel_Stat, null);
		
		panel_Stat.add(createDemoPanel());
		
		
		 ec = new Ecouteur();
		 
		 spinVie.addChangeListener(ec);
		 spinForce.addChangeListener(ec);
		 spinDext.addChangeListener(ec);
		 spinAgilite.addChangeListener(ec);
	
	
	
}

	public Joueur getJoueur() {
		return joueur;
	}
	public void setJoueur(Joueur joueur) {
		this.joueur = joueur;
	}
	public GestionCoolPoints getGestioncp() {
		return gestioncp;
	}
	public void setGestioncp(GestionCoolPoints gestioncp) {
		this.gestioncp = gestioncp;
	}
	
	public Statistiques getStatist() {
		return statist;
	}
	public void setStatist(Statistiques statist) {
		this.statist = statist;
	}	
	private class Ecouteur implements ChangeListener{

		@Override
		public void stateChanged(ChangeEvent e) {
			// TODO Auto-generated method stub
			
		}
}

	   private static PieDataset createDataset( ) {
		      DefaultPieDataset dataset = new DefaultPieDataset( );
		      dataset.setValue( "Gagné" , new Double( 40 ) );  
		      dataset.setValue( "Perdu" , new Double( 20 ) );     
		      return dataset;         
		   }
	
	   private static JFreeChart createChart( PieDataset dataset ) {
		      JFreeChart chart = ChartFactory.createPieChart(      
		         "Partis",   // le titre
		         dataset,          // donnee   
		         true,             // la legende  
		         true, 
		         false);
		      return chart;
		   }
	   
	   public static JPanel createDemoPanel( ) {
		      JFreeChart chart = createChart(createDataset( ) );  
		      ChartPanel chartpie = new ChartPanel(chart);
		      chartpie.setBounds(1, 50, 50, 50);
		      return chartpie; 
		   }
	   
	   
	
	
}

