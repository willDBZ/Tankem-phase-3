package Projet;

import java.awt.EventQueue;

import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JTextField;
import javax.swing.JButton;

/*Fait Par Humza*/
public class Connection extends JFrame {
	private JTextField textnom;
	private JTextField mdp;

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
		setBounds(100, 100, 300, 183);
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
		
		JButton btnconnection = new JButton("Connection");
		btnconnection.setBounds(185, 110, 89, 23);
		getContentPane().add(btnconnection);
		
		JButton btnAnnuler = new JButton("Annuler");
		btnAnnuler.setBounds(86, 110, 89, 23);
		getContentPane().add(btnAnnuler);

	}
}
