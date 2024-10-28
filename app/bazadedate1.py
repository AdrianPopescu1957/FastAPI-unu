
'''
Nume fisier:
    FastAPI\app\bazadedate1.py

Autor
    Adrian Popescu

Proiect
    management de documente cu Python prin FastAPI

Implementeaza
      FastAPI Environment Variables: Part #80 Python API Course de Sanjeev Thiyagarajan

Versiune anterioara
    FastAPI\app\bazadedate.py
    nou: introduce managementul variablelor "de mediu" (environment variables) pentru
    protejarea la executie a datelor sensibile cum este parola de acces la BD, dar si
    pentru facilitatea explotarii prin posibilitatea de configurare a denumirilor si
    amplasarii masinilor in mediul de productie
'''

#
#   Modulul pentru conectarea la BD PostgreSQL si manipularea datelor structurate 
#   de acolo (Modele de date, scheme SQLAlchemy)
#   Se foloseste cu modulul modele.py care descrie in limbaj Py (deci cu obiecte)
#   structurile de tabele din SGBDR si cu modulul config.py unde s-au strins
#   definitiile variabilelor "de mediu"
#
# acces la o BD tip postgresql in numele lui <username>, cu parola <password>
#  pe serverul de la adresa (sau cu numele) <ip-address/hostname>, baza de date cu 
#  numele <database-name>
#
# copiat ca atare din documentatia FastAPI/SQL (Relational) Databases!
# se asociaza cu modelul de date, structura descrisa in modulul separat numit modele.py
#
# legatura intre baza de date si modelul datelor continute se face in main.py!
#

'''
#Copiat din documentatia FastAPI
from sqlalchemy import create_engine                #importa "creatorul" de masini
from sqlalchemy.ext.declarative import declarative_base #importa creatorul de BD
from sqlalchemy.orm import sessionmaker             #importa "creatorul" de sesiuni

#SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
#SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
#formatul comenzii de creare a URL-ului pentru ORM SQLAlchemy la PostgreSQL:
#SQLALCHEMY_DATABASE_URL = "postgresql://user:password@Superadmin/db"
#           <database-name>" #creaza URL pentru ORM SQLAlchemy la PostgreSQL
#vezi numele utilizatorului si parola lui, numele serverului si numele BD folosite 
#   deja in main.py pentru a lucra cu BD direct prin driverul psycopg
#
#   S-a eliminat practica gresita a indicarii in clar a parolei utilizatorului
#   Incepind cu bazadedate1.py s-a implementat o practica buna!!
'''

from sqlalchemy import create_engine        #importa creatorul de masini (servere)
from sqlalchemy.orm import declarative_base #importa creatorul de BD
from sqlalchemy.orm import sessionmaker     #importa creatorul de sesiuni cu BD
from app.config import mediu     #stabilirea valori pentru mediul de lucru (nou din v1)

#sintaxa comenzii URL la BD PostgreSQL:
# SQLALCHEMY_DATABASE_URL = 
#       'postgresql://<username>:<password>@<ip-address/hostname>/<database-name>'
#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Superadmin@localhost:5432/fastapi' 
    #deoarece astea sint numele, parola, portul si adresa BD; 
    #!!! parola indicata aici in clar este o practica proasta, ca si INSERT in clar
#'''
# pentru teste
print("[bazadedate1] Citite din fisierul config.py: database_hostname = ",mediu.DB_hostname, ", database_port = ",
      mediu.DB_port, ", database_password = ",mediu.DB_password, ", database_name = ",mediu.DB_name, ", database_username = ",
      mediu.DB_username)    
#'''

#introduse variabilele pentru configurarea mediului de productie

database_hostname = mediu.DB_hostname
database_port = mediu.DB_port
database_password = mediu.DB_password
database_name = mediu.DB_name
database_username = mediu.DB_username

#print("[bazadedate1] Datele de acces la BD sint: database_hostname = ",database_hostname, ", database_port = ",
#      database_port, ", database_password = ",database_password, ", database_name = ",database_name, 
#      ", database_username = ",database_username) #pt test

#print("[bazadedate1] SQLALCHEMY_DATABASE_URL = ", f'postgresql://{database_username}:{database_password}@{database_hostname}:{database_port}/{database_name}')
SQLALCHEMY_DATABASE_URL = f'postgresql://{database_username}:{database_password}@{database_hostname}:{database_port}/{database_name}'
#print("[bazadedate1] SQLALCHEMY_DATABASE_URL = ", f'postgresql://{database_username}:{database_password}@{database_hostname}/{database_name}')
#SQLALCHEMY_DATABASE_URL = f'postgresql://{database_username}:{database_password}@{database_hostname}/{database_name}'


#pt o BD in memorie, nu pt. PostgreSQL:
#engine = create_engine(
#   SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}) 
masina = create_engine(SQLALCHEMY_DATABASE_URL) 
    #se stabileste conexiunea cu masina de date = se creaza masina SQLAlchemy 
    # pentru transformare obiectelor Python in comenzi PostgreSQL si invers

#creaza clasa sesiunilor de conectare la BD de pe masina:
SesiuneLocala = sessionmaker(autocommit=False, autoflush=False, bind=masina) 
    #creaza sesiunea de lucru cu masina, in anumite conditii date prin parametri

#creeaza clasa Baza
Baza = declarative_base() # acesta este obiectul BD propriu-zis ce va fi folosit 
    # de modelul (schema de date) pentru crearea tabelelor in interior

# defineste functia pt creerea legaturii (Dependency) cu BD, ca o sesiune deschisa 
#   pe BD; copie din documentatia FastAPI, lucrul cu PostgreSQL
#   deschide & inchide sesiune pe BD; de folosest oridecite ori CCSS pe BD
#   se apeleaza ca parametru in definitia functiei de operare cu API 
#   (Path operation function) asa:        db:Session = Depends(get_db)
#
def get_db():
    db = SesiuneLocala()
    try:
        yield db
    finally:
        db.close()

