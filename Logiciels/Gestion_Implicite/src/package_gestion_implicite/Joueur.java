package package_gestion_implicite;
/*FAIT PAR HUMZA*/
public class Joueur
{
	private String joueur;	
	private String phrase;
	private int couleurtank;


	private int r, g, b;
	private int xp;
	private int niveau;
	private String date;
	
	public Joueur(){}
	
	public Joueur(String joueur, String phrase, int couleurtank, int xp, int niveau, String date)	
	{
		this.joueur = joueur;
		this.phrase = phrase;
		this.couleurtank = couleurtank;
		this.xp = xp;
		this.niveau = niveau;
		this.date = date;
	}
	
	
	public String updatePrase(String updatePhrase){
		
		String phrase = getPhrase();
		/*Si la phrase est null du départ*/
		if (phrase == null)
		{
			setPhrase(updatePhrase);
			
			return getPhrase();
		}
		phrase = null;
		phrase = updatePhrase;
		
		return phrase;
	}
	
	public void updateCouleurTank(int r, int g, int b)
	{
		
		setR(r);
		setG(g);
		setB(b);
	}
	
	
	
	
	
	public void setJoueur(String joueur) {
		this.joueur = joueur;
	}


	public void setPhrase(String phrase) {
		this.phrase = phrase;
	}


	public void setCouleurtank( int r, int g, int b) {
	//	this.couleurtank = couleurtank;
		this.r = r;
  		this.g = g;
  		this.b = b;
	
	
		
	}
	
	public int getR() {
		return r;
	}


	public int getG() {
		return g;
	}


	public int getB() {
		return b;
	}
	

	public void setR(int r) {
		this.r = r;
	}


	public void setG(int g) {
		this.g = g;
	}


	public void setB(int b) {
		this.b = b;
	}

	
	public void setXp(int xp) {
		this.xp = xp;
	}


	public void setNiveau(int niveau) {
		this.niveau = niveau;
	}


	public void setDate(String date) {
		this.date = date;
	}
	
	public String getJoueur() {
		return joueur;
	}

	public String getPhrase() {
		return phrase;
	}

	public int getCouleurtank() {
		return couleurtank;
	}

	public int getXp() {
		return xp;
	}

	public int getNiveau() {
		return niveau;
	}

	public String getDate() {
		return date;
	}


}
