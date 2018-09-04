SET SERVEROUTPUT ON FORMAT WRAPPED;

-- supprimer les contraintes--
--alter table Partie drop constraint fk_id_Map;
alter table Armes_Stat drop constraint fk_id_Armes_Stat;
alter table Partie_Joueur drop constraint fk_id_Partie; 
alter table Partie_Joueur drop constraint fk_id_Joueur; -- 
alter table Armes_Stat drop constraint  fk_partie_joueur_id;
alter table Partie drop constraint  fk_id_gagnant; --


--supprimer les tables---

drop table Partie_Joueur CASCADE CONSTRAINTS;
drop table Partie CASCADE CONSTRAINTS;
drop table Joueur CASCADE CONSTRAINTS;
drop table Armes CASCADE CONSTRAINTS;
drop table Armes_Stat CASCADE CONSTRAINTS;

create table Partie_Joueur
(
  id NUMBER GENERATED ALWAYS as IDENTITY(START with 1 INCREMENT by 1),
  id_partie integer not null,
  id_joueur integer not null,
  distance number(6,2) not null,

constraint pk_id_Partie_Joueur primary key(id)

);



create table Partie
(
    id NUMBER GENERATED ALWAYS as IDENTITY(START with 1 INCREMENT by 1),
    Date_Debut Date not null,
    Date_Fin Date not null,
    id_Map integer not null,
    id_gagnant integer not null,

    constraint pk_id_Partie primary Key(id)
   
);




create table Joueur
(
  id NUMBER GENERATED ALWAYS as IDENTITY(START with 1 INCREMENT by 1),
  nom varchar2(15) unique not null,
  Vie integer  default(0) not null,
  Forces integer  default(0) not null,
  Agilite integer  default(0) not null,
  Dexterite integer  default(0) not null,
  Phrase_Joueur  varchar2(25) not null,
  Mot_De_Passe varchar2(20) not null,
  experience integer not null,
  Rouge integer,
  Vert integer,
  Bleu integer,
    CHECK(Rouge BETWEEN 0 and 255),
    CHECK(Vert BETWEEN 0 and 255),
    CHECK(Bleu BETWEEN 0 and 255),

constraint pk_id_Joueur primary key(id)
);




create table Armes
(
  id NUMBER GENERATED ALWAYS as IDENTITY(START with 1 INCREMENT by 1),
  nom varchar2(50)unique not null,

constraint pk_id_Arme primary key(id)

);

create table Armes_Stat
(
  id NUMBER GENERATED ALWAYS as IDENTITY(START with 1 INCREMENT by 1),
  id_Arme integer not null,
  Coup_Tire_Atteint_Cible integer  default(0),
  Coup_Recu integer  default(0),
  Coup_Total integer  default(0),
  partie_joueur_id integer not null,

constraint pk_id_Arme_Stat primary key(id)
);


--FK Table Partie Joueur
-- auteur: william et mathieu
alter Table Partie_Joueur
ADD Constraint fk_id_Partie foreign key(id_Partie) references Partie(id) DEFERRABLE INITIALLY DEFERRED;

alter Table Partie_Joueur
ADD Constraint fk_id_Joueur foreign key(id_Joueur) references Joueur(id);

-- FK Table Partie
alter Table Partie
ADD Constraint fk_id_Map foreign key(id_Map) references Map(id);

-- auteur:  william et mathieu
alter Table Partie
ADD Constraint fk_id_gagnant foreign key(id_gagnant) references Joueur(id) DEFERRABLE INITIALLY DEFERRED;


-- FK Table Armes_Stat
alter Table Armes_Stat
ADD Constraint fk_id_Armes_Stat foreign key(id_Arme) references Armes(id);

alter Table Armes_Stat
ADD Constraint fk_partie_joueur_id foreign key(partie_joueur_id) references Partie_Joueur(id);


-- Insertion du nom des armes

select * from Joueur;
select * from Partie;
select * from Partie_Joueur;
select * from Armes_Stat;
select * from Armes;




drop procedure insertNomArmesProcedure;

CREATE OR REPLACE PROCEDURE insertNomArmesProcedure
( nomArmes IN VARCHAR) AS
BEGIN
   INSERT INTO Armes(nom) VALUES(nomArmes);
END insertNomArmesProcedure;
/

execute insertNomArmesProcedure('Canon');
execute insertNomArmesProcedure('Mitraillette');
execute insertNomArmesProcedure('Grenade');
execute insertNomArmesProcedure('Piege');
execute insertNomArmesProcedure('Shotgun');
execute insertNomArmesProcedure('Guide');
execute insertNomArmesProcedure('Spring');
execute insertNomArmesProcedure('AucuneArme');

drop procedure insertJoueurProcedure;
CREATE OR REPLACE PROCEDURE insertJoueurProcedure
( nomJoueur IN VARCHAR,Vie IN integer,Forces IN integer, Agilite IN integer,Dexterite IN integer, Phrase_joueur IN VARCHAR,Mot_De_Passe IN VARCHAR,Experience IN integer,Rouge IN integer, Vert IN integer, Bleu IN integer) AS
BEGIN
   INSERT INTO Joueur(nom,vie,Forces,agilite,dexterite,phrase_joueur,mot_de_passe,experience,rouge,vert,bleu) VALUES(nomJoueur,Vie,Forces,Agilite,Dexterite,Phrase_joueur,Mot_De_Passe,Experience,Rouge,Vert,Bleu);
END insertJoueurProcedure;
/

--execute insertJoueurProcedure('a',2,2,2,2,'Je suis le Boss','1',1000,120,120,120);


drop procedure insertPartieProcedure;

CREATE OR REPLACE PROCEDURE insertPartieProcedure
( date_debut IN Date, date_fin IN DATE,id_Map IN INTEGER, id_gagnant IN INTEGER) AS
BEGIN
   INSERT INTO Partie(date_debut,date_fin,id_Map,id_gagnant) VALUES(date_debut,date_fin,id_Map,id_gagnant);
END insertPartieProcedure;
/



--execute insertPartieProcedure(TO_DATE('2003/05/03 21:02:44', 'yyyy/mm/dd hh24:mi:ss'), TO_DATE('2003/05/03 21:12:44', 'yyyy/mm/dd hh24:mi:ss'),1,1);

--TO_DATE('02-MAY-2018 12:50 PM', 'dd-mon-yyyy hh:mi PM');
--TO_DATE('2003/05/03 21:02:44', 'yyyy/mm/dd hh24:mi:ss');

--select * from Partie;

drop procedure insertArmes_StatProcedure;

CREATE OR REPLACE PROCEDURE insertArmes_StatProcedure
( id_arme IN INTEGER, Coup_Tire_Atteint_Cible IN INTEGER,Coup_Recu IN INTEGER, Coup_Total IN INTEGER, partie_Joueur_id IN INTEGER) AS
BEGIN
   INSERT INTO Armes_Stat(id_arme,Coup_Tire_Atteint_Cible,Coup_Recu,Coup_Total,partie_Joueur_id) VALUES(id_arme,Coup_Tire_Atteint_Cible,Coup_Recu,Coup_Total,partie_Joueur_id);
END insertArmes_StatProcedure;
/


drop procedure insertPartie_JoueurProcedure;

CREATE OR REPLACE PROCEDURE insertPartie_JoueurProcedure
( id_partie IN INTEGER, id_joueur IN INTEGER,distance IN INTEGER) AS
BEGIN
   INSERT INTO Partie_Joueur(id_partie,id_joueur,distance) VALUES(id_partie,id_joueur,distance);
END insertPartie_JoueurProcedure;
/

execute insertJoueurProcedure('a',2,2,2,2,'Je suis le Boss','a',1000,222,250,200);
execute insertJoueurProcedure('b',2,2,2,2,'Je suis le Boss','b',1000,255,250,200);



-- auteur: william 
-- but: procédure qui va insérer les informations sur la fin d'une partie

-- ( date_debut IN Date, date_fin IN DATE,id_Map IN INTEGER, id_joueur1 IN INTEGER, id_joueur2 IN INTEGER,distance1 IN INTEGER,distance2 IN INTEGER, id_partie_joueur1 OUT PARTIE_JOUEUR.ID%type, id_partie_joueur2 OUT PARTIE_JOUEUR.ID%type) AS

CREATE OR REPLACE PROCEDURE insertFin_PartieProcedure
( date_debut IN Date, date_fin IN DATE,id_Map IN INTEGER, id_joueur1 IN INTEGER, id_joueur2 IN INTEGER,distance1 IN INTEGER,distance2 IN INTEGER,experience1 IN INTEGER ,experience2 IN INTEGER,id_partie_joueur1 OUT PARTIE_JOUEUR.ID%type, id_partie_joueur2 OUT PARTIE_JOUEUR.ID%type) AS
    id_partie NUMBER;
BEGIN  
   DBMS_OUTPUT.PUT_LINE('Message: ' || 4 );
   INSERT INTO Partie(date_debut,date_fin,id_Map,id_gagnant) VALUES(date_debut,date_fin,id_Map,id_joueur1) returning ID into id_partie;
   INSERT INTO Partie_Joueur(id_partie,id_joueur,distance) VALUES(id_partie,id_joueur1,distance1) return ID into id_partie_joueur1;
   INSERT INTO Partie_Joueur(id_partie,id_joueur,distance) VALUES(id_partie,id_joueur2,distance2) return ID into id_partie_joueur2;
   update joueur set experience = experience1 where id = id_joueur1;
   update joueur set experience = experience2 where id = id_joueur2;
   DBMS_OUTPUT.PUT_LINE('Distance 1: ' || id_partie_joueur1);
   DBMS_OUTPUT.PUT_LINE('Distance 2: ' || id_partie_joueur2);
   DBMS_OUTPUT.PUT_LINE('Fini! ' );
   commit;
END insertFin_PartieProcedure;
/

commit;