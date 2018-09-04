package package_gestion_implicite;
/*Fait par Humza**/
public class GestionCoolPoints 
{

	private int cpTotaux;
	private int cpVie;
	private int cpForce;
	private int cpAgilite;
	private int cpDexterite;
	
	
	
	public GestionCoolPoints()
	{
		
	}
	
	public GestionCoolPoints(int cpTotaux, int cpVie, int cpForce, int cpAgilite, int cpDexterite) {
		this.cpTotaux = cpTotaux;
		this.cpVie = cpVie;
		this.cpForce = cpForce;
		this.cpAgilite = cpAgilite;
		this.cpDexterite = cpDexterite;
	}
	
	
	public void augmenter_coolpoints(int cpVie, int cpForce, int cpAgilite, int cpDexterite){
		int total = getCpTotaux();
		int vie= getCpVie();
		int force= getCpForce();
		int agilite = getCpAgilite();
		int dexterite = getCpDexterite();
		
		/*Modification des points sur la vie du joueur*/
		total -= cpVie;
		setCpTotaux(total);
		vie+= cpVie;
		setCpVie(vie);
		
		
		/*Modification des points sur la force du joueur*/
		total-= cpForce;
		setCpTotaux(total);
		force+= cpForce;
		setCpForce(force);
		
		
		/*Modification des points sur l'agilite du joueur*/
		total -= cpAgilite;
		setCpTotaux(total);
		agilite+= cpAgilite;
		setCpAgilite(agilite);
		
		/*Modification des points sur la dexterite du joueur*/
		total-= cpDexterite;
		setCpTotaux(total);
		dexterite = cpDexterite;
		setCpDexterite(dexterite);
		
	}
	
	public void diminuer_coolpoints(int cpVie, int cpForce, int cpAgilite, int cpDexterite){
		
		int total = getCpTotaux();
		total += cpVie;
		total += cpForce;
		total += cpAgilite;
		total += cpDexterite;
		
		setCpTotaux(total);
	}
	
	
	public void setCpTotaux(int cpTotaux) {
		this.cpTotaux = cpTotaux;
	}


	public void setCpVie(int cpVie) {
		this.cpVie = cpVie;
		
	}


	public void setCpForce(int cpForce) {
		this.cpForce = cpForce;
	}


	public void setCpAgilite(int cpAgilite) {
		this.cpAgilite = cpAgilite;
	}


	public void setCpDexterite(int cpDexterite) {
		this.cpDexterite = cpDexterite;
	}

	public int getCpTotaux() {
		return cpTotaux;
	}

	public int getCpVie() {
		return cpVie;
	}

	public int getCpForce() {
		return cpForce;
	}

	public int getCpAgilite() {
		return cpAgilite;
	}

	public int getCpDexterite() {
		return cpDexterite;
	}
	
	
	
	
	
	
	
	
	
	
}
