package package_gestion_implicite;
import java.awt.EventQueue;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JTextField;
import javax.swing.JButton;
import java.awt.Font;

/*Fait Par Humza*/
public class Connection extends JFrame {
	private JTextField textnom;
	private JTextField mdp;
	private JButton btnconnection;
	private JButton btnAnnuler;
	private Ecouteur ec;
	private Authentification aut;
	private Joueur j;
	private String nom;
	private JLabel lblmessage;
	private String mot;
	/**
	 * Launch the application.
	 */

	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					Connection frame = new Connection();
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
	public Connection() {
		setBounds(100, 100, 329, 183);
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		getContentPane().setLayout(null);
		
		JLabel lblNom = new JLabel("Nom : ");
		lblNom.setBounds(50, 33, 40, 14);
		getContentPane().add(lblNom);
		
		JLabel txtmdp = new JLabel("Mot de passe :");
		txtmdp.setBounds(10, 77, 80, 14);
		getContentPane().add(txtmdp);
		
		textnom = new JTextField();
		textnom.setBounds(90, 30, 86, 20);
		getContentPane().add(textnom);
		textnom.setColumns(10);
		
		mdp = new JTextField();
		mdp.setBounds(90, 74, 86, 20);
		getContentPane().add(mdp);
		mdp.setColumns(10);
		
		btnconnection = new JButton("Connection");
		btnconnection.setFont(new Font("Times New Roman", Font.PLAIN, 10));
		btnconnection.setBounds(185, 110, 89, 23);
		getContentPane().add(btnconnection);
		
		btnAnnuler = new JButton("Annuler");
		btnAnnuler.setBounds(86, 110, 89, 23);
		getContentPane().add(btnAnnuler);
		
		lblmessage = new JLabel("Le nom ou le mot de passe n'existe pas");
		lblmessage.setBounds(90, 8, 184, 14);
		getContentPane().add(lblmessage);
		lblmessage.setVisible(false); 
		
		ec = new Ecouteur();
		btnconnection.addActionListener(ec);
		btnAnnuler.addActionListener(ec);
		
	}
	
	public String getNom() {
		return nom;
	}



	public String getMot() {
		return mot;
	}
	
	public Authentification get_authentification()
	
	{
		
		return aut;
		
		
		
	}
	
	private class Ecouteur implements ActionListener
	{

		@Override
		public void actionPerformed(ActionEvent e) 
		{
			// TODO Auto-generated method stub
			
				if (e.getSource()== btnconnection)
				{
					
					if (!textnom.getText().equals("") && !mdp.getText().equals(""))
					{
						nom = textnom.getText().toString();
						mot = mdp.getText().toString();
						aut = new Authentification(nom, mot);
						j= new Joueur();
						j.setJoueur(nom);
						Connection.this.dispose();
						System.out.println(nom +"\n" + mot + "\n"+ j.getJoueur());
						
					}
					else
					{
						JOptionPane.showMessageDialog(Connection.this, "Entrez un nom d'usager et mot de passe");
					}
					
				}
				else if(e.getSource() == btnAnnuler)
				{
	                Connection.this.dispose();
				}
				
				
				else if(!textnom.getText().equals(aut.getNom()) && !mdp.getText().equals(aut.getMot_de_passe()))
				{
					
					lblmessage.setVisible(true); 
					
				}
		
		
		
		}
		
		
		public void messageErreur()
		{
			
			
		}
	

	public Authentification get_authentification()
	{
		
		return aut;
		
	}

	
		
		
		

	
	}
}
