/*  
    Projet: Tankem phase 2 (éditeur de jeu)
    Date de remise: 17 avril 2018
    Utilité: Remettre les tables à leur état par défaut
    Équipe: Mathieu D., Humza, Nephtalie, William
*/

/*  
    Respect des trois formes normales:
    1- 1FN: tous les champs de tous les tables sont atomiques. Ainsi, par exemple, dans la table Map,
    j'ai divisé les colonnes et rangees en deux champs, au lieu de les mettre dans le même champ.
    2- 2FN: la première forme normale est respectée. 
    Pour les tables type, status, map et joueur_maps, la clé primaire n'est composée que d'un seul champ. 
    La 2FN est automatiquement respectée, car chaque champ dépend entièrement de la clé primaire.
    Pour la table cases, qui a trois champs dans sa clé primaire, les champs non-clé dépendent des trois composantes
    de la clé primaire.
    3- 3FN: la deuxième forme normale est respectée. De plus, dans chaque table, un champ non clé ne dépend 
    nullement d'un autre champ non clé.

*/


-- Script des création des tables des niveaux de jeu
drop sequence map_seq;
drop sequence type_seq;
-- drop sequence cases_seq;
drop sequence status_seq;

drop trigger map_trig;
drop trigger type_trig;
drop trigger cases_trig;
drop trigger status_trig;

-- enlever les contraintes
alter table cases drop constraint fk_cases_map;
alter table cases drop constraint fk_cases_type;
alter table map drop constraint fk_map_status;
alter table joueur_map drop constraint pk_id_joueur_map;
alter table joueur_map drop constraint uqc_id_joueur_map;
alter table map drop constraint pk_id_map;

/*
drop table Cases;
drop table Map;
drop table type;
drop table status;
drop table joueur_map;
*/

drop table Cases CASCADE CONSTRAINTS;
drop table Map CASCADE CONSTRAINTS;
drop table type CASCADE CONSTRAINTS;
drop table status CASCADE CONSTRAINTS;
drop table joueur_map CASCADE CONSTRAINTS;


create table type
(
    id integer not null,
    nom varchar(30),
    
    constraint pk_id_type primary key(id)
);

create table status
(
    id integer not null,
    nom varchar(30),
    
    constraint pk_id_status primary key(id)
);

create table map
(
    id integer not null,
    titre varchar(20) not null unique,
    colonnes integer not null,
    rangees integer not null,
    dateCreation date,
    id_status integer not null,
    respawn_min float not null,
    respawn_max float not null,

    constraint pk_id_map primary key(id),
    constraint fk_map_status foreign key(id_status) references status(id)
);



create table cases
(
    id_map integer not null,
    id_type integer not null,
    colonne integer not null check(colonne > -1),
    rangee integer not null check(rangee > -1),
    arbre integer not null,
    

   constraint pk_id_cases primary key(id_map, colonne, rangee),
   constraint fk_cases_map foreign key (id_map) references map(id),
   constraint fk_cases_type foreign key(id_type) references type(id)
);

create table joueur_map
(
    id_map integer not null,
    colonne integer not null,
    rangee integer not null,
    ordre integer not null,
    
   constraint pk_id_joueur_map primary key(id_map, colonne, rangee)
);
ALTER TABLE joueur_map ADD CONSTRAINT uqc_id_joueur_map UNIQUE (id_map, ordre);


create sequence map_seq start with 1;
-- create sequence cases_seq start with 1;
create sequence type_seq start with 1;
create sequence status_seq start with 1;

create or replace trigger status_trig
before insert on status
for each row

begin
    select status_seq.nextval
    into :new.id
    from dual;
end;
/

-- remplir les status
insert into status(nom) values('Actif');
insert into status(nom) values('Inactif');
insert into status(nom) values('Test');

-- ins�rer la map al�atoire avant de cr�er le trigger
var titre varchar2(20);
exec :titre := 'Al�atoire';
insert into Map values(-1,:titre, 6, 6, sysdate, 1, 5, 20);

create or replace trigger map_trig
before insert on map
for each row

begin
    select map_seq.nextval
    into :new.id
    from dual;
end;
/

/*
create or replace trigger cases_trig
before insert on cases
for each row

begin
    select cases_seq.nextval
    into :new.id
    from dual;
end;
/
*/

create or replace trigger type_trig
before insert on type
for each row

begin
    select type_seq.nextval
    into :new.id
    from dual;
end;
/



create or replace trigger cases_trig
before update or insert
    on Cases
    for each row
declare 
    v_colonnes integer;
    v_rangees integer;
begin
    select colonnes into v_colonnes from map where id = :new.id_map;  
    select rangees into v_rangees from map where id = :new.id_map;  
    if :new.colonne > v_colonnes then    
        :new.colonne := NULL; -- pour g�n�rer une erreur
        dbms_output.put('Valeur qui d�passe la maximum.');
    end if;
    if :new.rangee > v_rangees then
        :new.rangee := NULL; -- pour g�n�rer une erreur
    end if;
end;
/

-- insertion des types de case possible
insert into type values(null,'plancher');
insert into type values(null,'murAnime');
insert into type values(null,'murAnimeInverse');
insert into type values(null,'murFixe');

-- faire des insertions (tests)



-- premiere map: ENFER
var titre varchar2(20);
exec :titre := 'Enfer';
insert into Map values(null,:titre, 6, 6, sysdate, 1, 5, 20);

insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murAnime'), 0,0,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murAnime'), 1,1,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murAnime'), 2,2,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murAnime'), 3,3,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murAnime'), 4,4,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murAnime'), 5,5,0);

insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murAnime'), 5,0,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murAnime'), 4,1,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murAnime'), 3,2,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murAnime'), 2,3,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murAnime'), 1,4,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murAnime'), 0,5,0);

insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'plancher'), 0,2,1);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'plancher'), 0,3,1);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'plancher'), 0,4,1);

insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'plancher'), 5,2,1);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'plancher'), 5,3,1);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'plancher'), 5,4,1);

-- insertion des joueur_maps
insert into joueur_map values((select id from map where titre = :titre),0,0,1);
insert into joueur_map values((select id from map where titre = :titre),5,5,2);


-- deuxieme map: PARADIS
var titre varchar2(20);
exec :titre := 'Paradis';
insert into Map values(null,:titre, 10, 10, sysdate, 1,1,3);

-- mur gauche
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 0,0,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 0,1,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 0,2,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 0,3,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 0,4,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 0,5,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 0,6,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 0,7,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 0,8,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 0,9,0);

-- mur droite
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 9,0,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 9,1,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 9,2,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 9,3,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 9,4,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 9,5,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 9,6,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 9,7,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 9,8,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 9,9,0);

-- mur haut
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 1,0,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 2,0,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 3,0,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 4,0,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 5,0,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 6,0,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 7,0,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 8,0,0);

-- mur bas
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 1,9,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 2,9,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 3,9,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 4,9,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 5,9,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 6,9,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 7,9,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 8,9,0);

-- milieu de la map
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'plancher'), 3,3,1);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'plancher'), 3,4,1);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'plancher'), 3,5,1);

insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'plancher'), 4,3,1);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'plancher'), 4,4,1);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'plancher'), 4,5,1);

insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'plancher'), 5,3,1);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'plancher'), 5,4,1);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'plancher'), 5,5,1);

-- insertion des joueur_maps
insert into joueur_map values((select id from map where titre = :titre),0,0,1);
insert into joueur_map values((select id from map where titre = :titre),9,9,2);

-- troisieme map: LABY TOWN
var titre varchar2(20);
exec :titre := 'Laby Town';
insert into Map values(null,:titre, 11, 6, sysdate, 1,3,15);

insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 1,1,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 1,2,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 1,3,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 1,4,1);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 1,5,1);

insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 5,1,1);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 5,2,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 5,3,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 5,4,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 5,5,1);

insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 9,1,1);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 9,2,1);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 9,3,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 9,4,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 9,5,0);

insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 3,0,1);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 3,1,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 3,2,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 3,3,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 3,4,1);

insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 7,0,1);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 7,1,1);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 7,2,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 7,3,0);
insert into Cases values((select id from map where titre = :titre), (select id from type where nom = 'murFixe'), 7,4,0);


-- insertion des joueur_maps
insert into joueur_map values((select id from map where titre = :titre),0,5,1);
insert into joueur_map values((select id from map where titre = :titre),10,5,2);

select * from map;
select * from type;
select * from cases where id_map = 9;
select * from cases;
select * from status;
select * from joueur_map;
select * from joueur_map where id_map = 1 order by ordre;

commit;


