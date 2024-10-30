#
#   Modulul pentru conectarea la BD PostgreSQL si manipularea datelor structurate 
#   de acolo
#   Se foloseste cu modulul modele.py care descrie in limbaj Py (deci cu obiecte)
#   structurile de tabele din SGBDR
#

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
#   Nu uita: indicarea in clar a parolei utilizatorului este o practica gresita
#   Vezi versiunile ulterioare pentru practica buna!!
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Superadmin@localhost/fastapi"

#engine = create_engine(
#   SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}) 
engine = create_engine(SQLALCHEMY_DATABASE_URL) # creaza masina SQLAlchemy 
            # pentru transformare obiectelor Python in comenzi PostgreSQL si invers
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #Fiecare 
        #instanta a clasei SessionLocal va fi o sesiune deschisa pe BD; este numita 
        #SessionLocal pentru a o deosebi de Session importata din SQLAlchemy
        #atentie la parametrii commit ai BD!!

Base = declarative_base()   #creaza clasa Base ca BD

