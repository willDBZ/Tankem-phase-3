drop procedure INS_ARMES;

CREATE OR REPLACE PROCEDURE INS_ARMES 
(
  INS_ID IN NUMBER 
, INS_NOM IN VARCHAR2 
) AS 
BEGIN
  null;
END INS_ARMES;

select nom from Armes;
insert into Armes(id,nom) Values('9', 'Test');

select nom from Armes where id = '1';


//////////////////////////
create table test
(
    id integer not null,
   nom varchar2(20) not null,
    constraint pk_id_test primary Key(id)
   
);

insert into test (id,nom) Values('2','Benoit');
select * from test;

/////////////////

**********************
drop procedure remove_emp;
create procedure remove_emp (id NUMBER) AS
tot_emps NUMBER;
Begin
    delete From Test
    where test.id = remove_emp.id;
tot_emps := tot_emps -1;
END;
/

execute remove_emp(1);
execute remove_emp(2);

*************
commit;