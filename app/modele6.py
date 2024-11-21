'''
Nume fisier:
    FastAPI\app\modele6.py

Autor
    Adrian Popescu

Proiect
    management de documente cu Python prin FastAPI

Implementeaza
    FastAPI Votes/like Theory file: Part #81 Python API Course de Sanjeev Thiyagarajan
    FastAPI Creating Votes Table pgadmin file: Part #82 Python API Course de Sanjeev Thiyagarajan
    FastAPI Votes SQLAlchemy file: Part #83 Python API Course de Sanjeev Thiyagarajan
    FastAPI Votes Route file: Part #84 Python API Course de Sanjeev Thiyagarajan

Versiune anterioara
    FastAPI\app\modele5.py

Introduce:
    votarea (tabela pentru voturi)   
'''
#
#   Modulul pentru descrierea modelelor (structurilor de date) in limbaj (cu obiecte) Python
# creaza modelul de date pentru baza de date Baza definita in modulul bazadedate.py
#                   Operare cu ORM Alchemy      (Modele de date, scheme SQLAlchemy)
#   Folosit impreuna cu modulul bazadedate.py care a initiat elementele de conectare
#       la SGBDR PostgreSQL, sesiunea de lucru cu BD si clasa obiectelor Baza care sint BD-uri
#   Practic, creaza tabelele in BD;  Fiecare model = o tabela in BD
#       Atentie! Creaza o tabela daca ea nu exista; daca tabela exista nu va verifica existenta
#               si proprietatile coloanelor, deci, daca este necesara extinderea tabelei este
#               necesara folosirea altor utilitare (utilitare pentru "migrare")
#
#    legatura intre baza de date si modelul datelor continute se face in main.py
#
#   modificat din modele.py pentru main7.py

# Foloseste clasa Baza creata (anterior) in modulul bazadedate.py (ultima linie!)
from sqlalchemy import MetaData
from sqlalchemy import Column   #importa definitiile clasei Column pt a def coloanele tabelei
from sqlalchemy import Integer  #importa definitia intregilor compatibila cu Python
from sqlalchemy import String  #importa definitia sirurilor de caractere compatibila cu Python
from sqlalchemy import Boolean  #importa definitia Bool de caractere compatibila cu Python
from sqlalchemy import ForeignKey  #importa definitia cheilor straine pt relatii intre tabele
from sqlalchemy.orm import Relationship  #importa definitia cheilor straine pt relatii intre tabele
from datetime import datetime #modulul operatiilor cu timpul; folosit pt a inregistra momentul operatiunii
from bazadedate1 import Baza  #importa din bazadedate.py obiectul (=clasa) Baza
from bazadedate1 import masina  #importa din bazadedate.py masina



#folosind ORM-ul SQLAlchemy creem clasa Post in la "interfata" cu clasa Articol
class Post(Baza):   #creaza clasa Post de tip Baza, in fapt tabel posts din BD
                    #tabela posts va fi creata de acest program in BD, pe linga tabela 
                    #articole si clasa Articole cu care am exersat pina acum
    __tablename__ = "posts" 
    id = Column(Integer, primary_key=True, nullable=False)  #nevid, cheie primara, nr.intreg
    titlu = Column(String, nullable=False)  #cimp nevid, tip sir de caractere
    ciorna = Column(Boolean, default=True)  #cimp optional, implicit "articol nepublicabil"
    continut = Column(String, default='Continutul articolului') #continutul p.-zis al artic.
    apreciere = Column (Integer)    #cimp optional, tip intreg
        #data si ora mai tirziu
    idproprietar = Column (Integer, ForeignKey(column="users.id", ondelete="CASCADE"),
                    nullable=False) 
        #cimp creat odata cu modele3.py pentru a lega articolele
        # din tabela de utilizatori prin id din tabela users; + cheie indispensabila,
        # de exact acelasi tip cu id din tabela users; + daca utilizatorul dispare, automat
        # se distrug articolele cu id-ul lui
    proprietar = Relationship("User")   # extrage info despre utilizator din clasa User(Baza)
        #pentru a-i vedea efectele trebuie sa actualizezi corespunzator validari.py

class User(Baza):   #creaza clasa User de tip Baza, in fapt tabel users in BD
                    #tabela users va fi creata de acest program in BD, pe linga tabela 
                    #articole si clasa Articole, posts si clasa POST cu care am exersat pina
                    # la modele.py pentru main6.py si anterioarele
    __tablename__ = "users" 
    id = Column(Integer, primary_key=True, nullable=False)  #nevid, cheie primara, nr.intreg
    email = Column(String, nullable=False, unique=True)  #practic numele utilizatorului = email
    parola = Column(String, nullable=False) #parola
    moment = Column (String, nullable=False, server_default=str(datetime.now()))  #momentul creerii
#    telefon = Column(String, nullable=False)
#    telmobil = Column(String, nullable=False)

class Vot(Baza): #creaza clasa Vot de tip Baza, in fapt tabela voturi in BD
                 #in cazul in care o tabela Vot lipseste, ea va fi creata prinexecutia acestui modul,
                 #pe linga cele de mai sus
    __tablename__ = "voturi"
    iduser = Column (Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True) 
    idart = Column (Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)

#creaza tabelele in Baza de pe masina; obligatoriu daca nu BD nu exista!!
Baza.metadata.create_all(bind=masina)
#   !!este inutila in cazul in care BD dorita exista, de ex. cazul creerii/migrarii cu Alembic!! 

metadata=MetaData()
