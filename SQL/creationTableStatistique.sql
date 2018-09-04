
-- supprimer les contraintes--
--alter table Partie drop constraint fk_id_Map;
alter table Armes_Stat drop constraint fk_id_Armes_Stat;
alter table Partie_Joueur drop constraint fk_id_Partie;
alter table Partie_Joueur drop constraint fk_id_Joueur;
alter table Armes_Stat drop constraint  fk_partie_joueur_id;

alter table Partie drop constraint  fk_id_gagnant;


--supprimer les tables---

drop table Partie_Joueur;
drop table Partie;
drop table Joueur;
drop table Armes;
drop table Armes_Stat;


create table Partie_Joueur
(
  id integer not null,
  id_partie integer not null,
  id_joueur integer not null unique,
  distance integer not null,

constraint pk_id_Partie_Joueur primary key(id)

);



create table Partie
(
    id integer not null,
    Date_Debut Date not null,
    Date_Fin Date not null,
    id_Map integer not null,
    id_gagnant integer not null,

    constraint pk_id_Partie primary Key(id)
   
);




create table Joueur
(
  id integer not null,
  nom varchar2(50) unique not null,
  Vie integer  default(0) not null,
  Force integer  default(0) not null,
  Agilite integer  default(0) not null,
  Dexterite integer  default(0) not null,
  Phrase_Joueur  varchar2(50) not null,
  Mot_De_Passe varchar2(50) not null,
  experience integer not null,
  Rouge integer,
  Vert integer,
  Bleu integer,

constraint pk_id_Joueur primary key(id)
);




create table Armes
(
  id integer not null,
  nom varchar2(50),

constraint pk_id_Arme primary key(id)

);

create table Armes_Stat
(
  id integer not null,
  id_Arme integer not null,
  Coup_Tire_Atteint_Cible integer  default(0),
  Coup_Recu integer  default(0),
  Coup_Total integer  default(0),
  partie_joueur_id integer not null,

constraint pk_id_Arme_Stat primary key(id)
);


-- création des dummies
insert into Partie_Joueur (id, id_partie, id_joueur, distance) values(0,0,0,0);
insert into partie (id, date_debut, date_fin, id_map, id_gagnant) values(0,sysdate,sysdate,0,0);
insert into joueur (id, nom, vie, force ,agilite, dexterite, phrase_joueur, mot_de_passe, experience) values(0,'bidon',0,0,0,0,'bidon','bidon',0);

--FK Table Partie Joueur
alter Table Partie_Joueur
ADD Constraint fk_id_Partie foreign key(id_Partie) references Partie(id);

alter Table Partie_Joueur
ADD Constraint fk_id_Joueur foreign key(id_Joueur) references Joueur(id);

-- FK Table Partie
alter Table Partie
ADD Constraint fk_id_Map foreign key(id_Map) references Map(id);

alter Table Partie
ADD Constraint fk_id_gagnant foreign key(id_gagnant) references Partie_Joueur(id_joueur);

-- FK Table Armes_Stat
alter Table Armes_Stat
ADD Constraint fk_id_Armes_Stat foreign key(id_Arme) references Armes(id);

alter Table Armes_Stat
ADD Constraint fk_partie_joueur_id foreign key(partie_joueur_id) references Partie_Joueur(id);


-- Insertion du nom des armes

insert into Armes values(1,'Canon');
insert into Armes values(2,'Mitraillette');
insert into Armes values(3,'Grenade');
insert into Armes values(4,'Piege');
insert into Armes values(5,'Shotgun');
insert into Armes values(6,'Guide');
insert into Armes values(7,'Spring');
insert into Armes values(8,'AucuneArme');

select * from Joueur;
select * from Partie;
select * from Partie_Joueur;
select * from Armes_Stat;
select * from Armes;









commit;