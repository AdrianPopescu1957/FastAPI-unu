'''
Nume fisier:
    FastAPI\app\main17.py

Autor
    Adrian Popescu

Proiect
    management de documente cu Python prin FastAPI

Implementeaza
    FastAPI What is CORS: Part #?? Python API Course de Sanjeev Thiyagarajan

Versiune anterioara
    FastAPI\app\main16.py
    nou: introduce permisiunea de acces dinafara domeniului Internet propriu
'''
#
#   Citeste, scrie, actualizeaza si sterge "articole" si "useri" 
#       dintr-o BD PostgreSQL cu ORM folosind module separate pentru:
#           interfata pentru gestiunea utilizatorilor,
#           validarea datelor comunicate cu serverul,
#           gestiunea datelor din BD,
#           functii auxiliare
#   Versiune evoluata din main13.py pentru pregatirea executiei in mediul de productie
#       difera de curs prin aceea ca BaseSettings se ia din pydantic_settings
#       
#   Conventii: articole (am tradus posts nu prin postari ci prin articole sau postari), 
#           utilizatori (la plural), /articole (URL-uri), POST REQUEST (ordin de publicare)

from fastapi import FastAPI #importata biblioteca necesara pentru crearea obiectelor de tip FastAPI
from datetime import datetime  #modului operatiilor cu timpul; folosit pt test versiune server
from .rute import autentif4, useri5, articole7, voturi1  # rute separate spre functii diferite
from fastapi.middleware.cors import CORSMiddleware


#from config import mediu #modulul variabilelor de mediu pentru dezvoltare si exploatare
#from bazadedate1 import masina  #importa din bazadedate.py masina
#from modele6 import Baza
#Baza.metadata.create_all(bind=masina)    #creaza tabelele in Baza de pe masina
        ## am folosit-o in bazadedate.py, modele .py vezi cum interfereaza cu Alembic!!

#creata o instanta API = un obiect FastAPI
app = FastAPI() #conecteaza navigatorul Internet cu sit-ul Internet =
                #   = creaza obiectul "aplicatie de interfata de acces la sit Internet"

#adaugat middlware pentru Cross Origin Resouce Sharing
#origins = ["http://localhost.tiangolo.com", "https://localhost.tiangolo.com",
#    "http://localhost", "http://localhost:8080","https://www.google.com",]pip 
origins = ["*"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],)
#       CORSMiddleware      functie care este executata inaintea oricarei cereri, pentru a 
#                              verifica drepturile de acces ale initiatorului cererii (originea)
#       allow_origins       lista domeniilor carora li se permite accesul la app: aici
#                               originile pot fi in google.com, tiangolo.com...;
#                                ["*"] => toate
#       allow_credentials   daca se solicita prezentarea de credentiale pentru a permite accesul
#       allow_methods       lista metodelor de acces la app permise; ["*"] => toate
#       allow_headers       lista hederelor permise; ["*"] => toate

#
# SECTIUNEA operatiilor FastAPI; 
#           operatie FastAPI = perechea actiune (=metoda) + cale acces(=path+param);
#   !!! Accesul la datele din BD PostgreSQL se face prin driverul psyconfig !!!
#
# ATENTIE! la succesiune: se cauta in cod de sus in jos si se aplica prima 
#                           pereche metoda + parametur gasita intre definitii
#
#   din v9 au fost separate caile de acces pentru utilizatori si pentru articolele p.zise, adica
#   au fost create rute speciale pentru accesul separat la resursele pentru mamagementul
#    utilizatorilor, articolelor (postari, date propriu-zise) si operatiilor de autentificare

#
#  ZONA   Manipularea datelor din BD din server cu tratarea "exceptiilor" 
#     (stari nedorite dar posibile!) a fost mutata din v9 in /rute, in articoleX.py si useriX.py
#       metoda login (cu JWT bearer) este in autentifx.py (cu oauth2x.py)
#

app.include_router(articole7.ruter)  #ruta spre caile de operare a articolelor (posts)
print('[main17] app.include_router(useri5.ruter)')
app.include_router(useri5.ruter)  #ruta spre caile de operare a utilizatorilor (user-i)
app.include_router(autentif4.ruter)  #ruta spre metodele login (JWT bearer)
app.include_router(voturi1.ruter)  #ruta spre metodele pentru votare (voturi)


# Metoda GET este actiunea de trimitere catre serverul API a caii ("path" = adresa datelor) si,
#   eventual, a parametrilor de interogare a datelor, pentru date 'nestructurate' adica 
#   (siruri, intregi, liste..);

# 0. Verifica functionarea serverului (o folosesc doar pentru testare)
#   Read    -> GET          /       @app.get("/")
#
@app.get("/")  #metoda get = preia date din pagina publicata in radacina
async def vadserver():     # intoarce un semn de la server
    return {"  Salut, sint serverul main17.py! Este ora: ", datetime.now()}    

