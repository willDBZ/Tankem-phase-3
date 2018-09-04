create or replace trigger trg_phrase_Joueur
before update or insert
    
	on Joueur    
	for each row 

declare 
    caracteres number; 
	    valMax number = 50;

begin
    
	caracteres := :new.valmax;
    
     
        
    

	if(length(:new.phrase_Joueur) > valMax) then
           
		 :new.phrase_Joueur :=substr(:new.phrase_joueur,0,valMax);
       
		 end if;
      
    
	end;

commit;

sinon utiliser un substr




drop procedure insertJoueurProcedure;
CREATE OR REPLACE PROCEDURE insertJoueurProcedure
( nomJoueur IN VARCHAR,Vie IN integer,Forces IN integer, Agilite IN integer,Dexterite IN integer, Phrase_joueur IN VARCHAR,Mot_De_Passe IN VARCHAR,Experience IN integer,Rouge IN integer, Vert IN integer, Bleu IN integer) AS
BEGIN
   INSERT INTO Joueur(nom,vie,Forces,agilite,dexterite,phrase_joueur,mot_de_passe,experience,rouge,vert,bleu) VALUES(nomJoueur,Vie,Forces,Agilite,Dexterite,Phrase_joueur,Mot_De_Passe,Experience,Rouge,Vert,Bleu);
END insertJoueurProcedure;
/


drop procedure phrase_joueur_Procedure;
create or replace procedure phrase_joueur_procedure;

DECLARE
       lv_training_code_txt VARCHAR2(10) := 'T_Code';
       lv_non_training_code_txt VARCHAR2(10) := 'TUSC';
       PROCEDURE training_class_check (p_class_check VARCHAR) IS p_class_check1 VARCHAR2(10) := p_class_check;
    BEGIN
          IF SUBSTR(p_class_check1,1,2) = 'T_' THEN
             p_class_check1 := 'T-' || SUBSTR(p_class_check1, 3);
          END IF;
          IF p_class_check1 LIKE 'T-%' THEN
            DBMS_OUTPUT.PUT_LINE(p_class_check ||' is a Training Class');
         ELSE
            DBMS_OUTPUT.PUT_LINE(p_class_check ||' is a Non-Training Class');
         END IF;
   END training_class_check;
 
   BEGIN
      training_class_check(lv_training_code_txt);
      training_class_check(lv_non_training_code_txt);
   END;
  /