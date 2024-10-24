'''
Nume fisier:
    FastAPI/app/rute/useri5.py

Autor
    Adrian Popescu

Proiect
    management de documente cu Python prin FastAPI

Implementeaza    
    FastAPI Votes/like Theory file: Part #81 Python API Course de Sanjeev Thiyagarajan
    FastAPI Creating Votes Table pgadmin file: Part #82 Python API Course de Sanjeev Thiyagarajan
    FastAPI Votes SQLAlchemy file: Part #83 Python API Course de Sanjeev Thiyagarajan
    FastAPI Votes Route file: Part #84 Python API Course de Sanjeev Thiyagarajan
    FastAPI SQL Joins/ SQLAlchemy file: Part #86 Python API Course de Sanjeev Thiyagarajan
'''
#Versiune anterioara
#    FastAPI\app\rute\useri4.py
#nou: Votarea


from fastapi import APIRouter #pt rutele de acces la resurse, necesar pt separare user si articol
from fastapi import status #biblio pentru codurile standard http ale serverului, folosit cu Response
from fastapi import HTTPException #trateaza semnalele de eroare http, ! in loc de Response + status
from fastapi import Depends #trateaza conexiunile cu sesiunea de lucru cu DB prin ORM
## !! NOU APIRouter din fastapi
## !! Inlocuieste obiectul app definit in main.py cu un obiect local de tip ruter

from typing import List #transforma in liste obiecte exprimate ca in BD
from sqlalchemy.orm import Session  #preia definitia sesiunii pe o BD din ORM-ul SQLAlchemy
from datetime import datetime

from validari8 import CreUser, FiltruUser  #preia definitia modelelor de date din validari6.py
from validari8 import ModifNume, ModifParola  #preia definitia modelelor de date din validari6.py
from rute.oauth26 import iausercurent  #preia metoda idutilizator din oauth24.py 
from bazadedate1 import get_db  #importa din bazadedate.py metoda de open/close DB session
from modele6 import User  #preia definitia modelelor de date din modele4.py
from util1 import hash   #preia definitia pentru criptarea sirurilor de caractere

#s-a inlocuit obiectul app de tip FastAPI din main.py cu un obiect de acelasi tip apelabil
#  dintr-o pozitie superioara a ierarhiei  de fisiere (module py)
ruter = APIRouter(    #  introdus in v10 pentru limpezirea documentatiei
            prefix= "/users",      #scurtata denumirea caii de acces inlocuind /users cu /
            tags= ['Management utilizatori'])  #grupate metodele pt user mgmt

# Citeste intregul continut al tabelei Users al BD 
#
@ruter.get("/", response_model= List[FiltruUser])  #metoda get = preia toate datele
async def iadinusers(db:Session = Depends(get_db)): 
        #functia intoarce toate rindurile tabelei users deschise si inchise cu get_db
        # List transforma obiectul BD intr-o lista ce se poate trimite clientului
    inreg = db.query(User).all()   #interogheaza in modelul de date User 
            #din modele4.py adica din tabela posts a BD, in sesiunea creata de 
            #dependenta creata prin get_db, toate rindurile <= all() tabelei
    return inreg  #zice ca raspunsul este mai curat astfel
'''
''' 

# 7. Creaza un utilizator nou inregistrind in tabela users a BD PostgreSQL 
#       cu ORM-ul SQLAlchemy, copiat din creare nou articol de publicat
@ruter.post("/", status_code= status.HTTP_201_CREATED, response_model=FiltruUser)
                #si filtreaza raspunsul catre client
async def creazauser(inreg:CreUser, db:Session = Depends(get_db)):
    #print ("sint creaza user, parola primita este", inreg.parola) #pt test
    inreg.parola = hash (inreg.parola)  #cripteaza cimpul parola cu o functie de tip hash
    #print ("sint creaza user, parola criptata este", inreg.parola) #pt test
    inreg = User (**inreg.dict()) #excelent, sintaxa speciala echivalenta!!
# !! trebuie tratat cazul in care se incearca crearea unui user deja existent !!
#       as folosi codul de la UPDATE articol
    db.add(inreg)
    db.commit()
    db.refresh(inreg)
    #return {"Sint serverul; in BD s-a inregistrat": inreg}
    return inreg   #zice ca raspunsul este mai curat astfel
        #merge asa fiindca FastAPI stie sa transforme acest obiect intr-unul de tip lista
'''
Daca clientul cu:     http://127.0.0.1:8000/users/
trimite: {"email": "ana@gmail.com","parola": "werewrt"}
serverul il accepta cu numele intern inreg de tip Articol si cu:     return inreg
    intoarce: {"id":4,"email":"ana@gmail.com"}
cu starea: 201 Created 
The request has been fulfilled and resulted in a new resource being created

Daca clientul cu:     http://127.0.0.1:8000/users/
trimite: {"email": "ana@.com","parola": "werewrt"}
serverul nu il accepta si cu:     return inreg
    intoarce: {"id":4,"email":"ana@gmail.com"}
{"detail":[{"type":"value_error","loc":["body","email"],"msg":"value is not a valid email 
    address: An email address cannot have a period immediately after the @-sign.",
    "input":"ana@.com","ctx":{"reason":"An email address cannot have a period immediately after
    the @-sign."}}]}
cu starea: 422 Unprocessable Entity The request was well-formed but was unable 
    to be followed due to semantic errors
'''

# 8. Citeste datele despre un utilizator folosind id-ul sau
#   Read    -> GET          /       @ruter.get("/ceva/{parametru}")
#   copiata metoda similara pentru articole
@ruter.get("/{id}", response_model= FiltruUser)  
# metoda get = intoarce clientului art cu id cerut, filtrat
async def iauser(id:int, db:Session = Depends(get_db)): #vede id, trimite date si stari
    inreg = db.query(User).filter(User.id == id).first()  #cauta in tabela users a BD, in
            # sesiunea deschisa pe BD prin metoda get_db, prima intilnire a inreg id
            # fiindca id e unic, nu cauti mai departe (=all) ci opresti cautarea (<=first)
    if inreg == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                detail = f"Mesaj de la server: utilizatorul cu id: {id} nu este cunoscut in BD")
    return inreg    # FastAPI stie sa faca lista dintr-o inreg. filtrata din DB
#Apelat in navigator=client cu: http://127.0.0.1:8000/users/3
#   Intoarce: ["Sint serverul; articolul cu id",3,"in BD este:{"id": 15,"email": "misu@mfinante.gov.ro"}
#   cu starea: 200 Ok Standard response for successful HTTP requests. The actual response 
#   will depend on the request method used. In a GET request, the response will contain 
#   an entity corresponding to the requested resource. In a POST request the response will 
#   contain an entity describing or containing the result of the action
#Apelat in navigator=client cu: http://127.0.0.1:8000/users/101
#   Intoarce: {"detail": "Mesaj de la server: utilizatorul cu id: 101 nu este cunoscut in BD"}
#   cu starea: 404 Not Found  The requested resource could not be found but may be available
#    again in the future. Subsequent requests by the client are permissible.
#Apelat in navigator=client cu: http://127.0.0.1:8000/users/osuta
#   Intoarce: {"detail":[{"type":"int_parsing","loc":["path","id"],"msg":"Input should be a valid integer, 
#   unable to parse string as an integer","input":"osuta","url":"https://errors.pydantic.dev/2.5/v/int_parsing"}]}
#   cu starea: 422 Unprocessable Entity The request was well-formed but was unable 
#   to be followed due to semantic errors


# 9. Actualizeaza numele utilizatorului in BD de pe server
# folosind datele de id din jetonul JWT prezentat in cerere
#   Update    -> PUT  /users @ruter.put("/ceva")
#   copiata metoda similara pentru articole
# functia modifica articolul cu id luat din jeton de autentificare (cimpurile email si moment)
#  prin numenou: ModifNumese folosesc functiile de verificare a datelor primite in nume

@ruter.put("/modifnume", status_code= status.HTTP_200_OK, response_model= FiltruUser)  
# metoda put = modifica date si intoarce clientului user cu id cerut, filtrat
async def refacnume(numenou:ModifNume, db:Session = Depends(get_db),  
            usercurent: int = Depends (iausercurent)): #gaseste id, modifica date
    #print("[1.din useri2.refacnume] id utilizator curent (int): ", usercurent, 
    #      "nume nou numenou.email ", numenou.email)   #pentru test
    sqlinreg = db.query(User).filter(User.id == usercurent)  #creaza SQL pentru cautare in 
            # tabela users a BD, in sesiunea deschisa pe BD prin metoda get_db
    inreg = sqlinreg.first()    # executa SQL pentru prima intilnire a inreg id
            # fiindca id e uni opresti cautarea (<=first) la prima valoare gasita
    if inreg == None:   # daca nu exista inregistrarea !!INUTIL, semnalat de la autentificare
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, 
                detail = f"Mesaj de la server: actiune neautorizata")
    if inreg.id != usercurent:  #verifica dreptul de acces la inregistrare (!!! INUTIL, idem !!!)
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, 
                detail = f"Mesaj de la server:  actiune neautorizata")
    #print("[2.din useri2.refacnume] utilizator care se modifica :", inreg.id, inreg.email, inreg.parola)  #pt test
    inreg.email = numenou.email #modificare cimp nume utilizator (in fapt nume = email)
    inreg.moment = datetime.now()   #actualizare data
    #print("[3.din useri2.refacnume] utilizator.email e:",inreg.email, "utilizator.moment: ", inreg.moment) #pt test
    db.add(inreg)   #modificare inreg in memo
    db.commit()     #inregistrare pe disc
    db.refresh(inreg)   #refacere info pe discuri (de ce?)
    return inreg    # FastAPI stie sa faca lista dintr-o inreg. filtrata din DB

#Daca se apeleaza in navigator=client cu: http://127.0.0.1:8000/postari/3
#   si body apel: {"titlu": "Titlul nou","continut": ["linia 1","linia 2","sfirsit"]}
# clientul primeste:
#   ["Mesaj de la server: articolul cu id",3,"a fost modificat in",{"titlu":"Titlul nou",
#   "ciorna":true,"id":3,"continut":"{\"linia 1\",\"linia 2\",sfirsit}","apreciere":null}]
#   cu starea: 200 Ok Standard response for successful HTTP requests. The actual response 
#   will depend on the request method used. In a GET request, the response will contain 
#   an entity corresponding to the requested resource. In a POST request the response will 
#   contain an entity describing or containing the result of the action
#Daca se apeleaza in navigator=client cu: http://127.0.0.1:8000/postari/44
#   si body apel: {"titlu": "Titlul nou","continut": ["linia 1","linia 2","sfirsit"]}
# clientul primeste:
#  {"detail":"Mesaj de la server: articolul cu id: 1 nu se gaseste in BD"}
#   cu starea: 404 Not Found The requested resource could not be found but may be 
#   available again in the future. Subsequent requests by the client are permissible
#Daca se apeleaza in navigator=client cu: http://127.0.0.1:8000/postari/sd
#   si body apel: {"titlu": "Titlul nou","continut": ["linia 1","linia 2","sfirsit"]}
# clientul primeste:
#   {"detail":[{"type":"int_parsing","loc":["path","id"],"msg":"Input should be a valid 
#   integer, unable to parse string as an integer","input":"sd",
#   "url":"https://errors.pydantic.dev/2.5/v/int_parsing"}]}
#   cu starea: 422 Unprocessable Entity The request was well-formed but was unable 
#   to be followed due to semantic errors    
#Daca se apeleaza in navigator=client cu: http://127.0.0.1:8000/postari/sd
#   si body apel: {"titlu": "Titlul nou ceva mai lung decit e admis","continut": 
#   ["linia 1","linia 2","sfirsit"]}
# clientul primeste:
#   {"detail":[{"type":"string_too_long","loc":["body","titlu"],
#   "msg":"String should have at most 23 characters",
#   "input":"Titlul  nou ceva mai lung decit admis","ctx":{"max_length":23},
#   "url":"https://errors.pydantic.dev/2.5/v/string_too_long"}]}
#   cu starea: 422 Unprocessable Entity The request was well-formed but was unable 
#   to be followed due to semantic errors

# 10. Actualizeaza parola utilizatorului in BD de pe server, recunoastrerea utilizatorului
# folosind datele de id din jetonul JWT prezentat in cerere
#   Update    -> PUT  /users @ruter.put("/ceva")
#   copiata metoda PUT de mai sus pentru modificare nume (=email)
# functia modifica articolul cu id luat din jeton de autentificare (cimpurile parola si moment)
#  prin numenou: ModifParola folosesc functiile de verificare a datelor primite in nume

@ruter.put("/modifparola", status_code= status.HTTP_200_OK, response_model= FiltruUser)  
# metoda put = modifica date si intoarce clientului user cu id cerut, filtrat
async def refacparola(parolanoua:ModifParola, db:Session = Depends(get_db),  
            usercurent: int = Depends (iausercurent)): #gaseste id, modifica date
    print("[1.din useri2.refacparola] utilizator curent (int): ", usercurent, 
          "parola dorita parolanoua.parola ", parolanoua.parola)   #pentru test
    sqlinreg = db.query(User).filter(User.id == usercurent)  #creaza SQL pentru cautare in 
            # tabela users a BD, in sesiunea deschisa pe BD prin metoda get_db
    inreg = sqlinreg.first()    # executa SQL pentru prima intilnire a inreg id
            # fiindca id e uni opresti cautarea (<=first) la prima valoare gasita
    if inreg == None:   # daca nu exista inregistrarea !!INUTIL, semnalat de la autentificare
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, 
                detail = f"Mesaj de la server: actiune neautorizata")
    if inreg.id != usercurent:  #verifica dreptul de acces la inregistrare (!!! INUTIL, idem !!!)
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, 
                detail = f"Mesaj de la server:  actiune neautorizata")
    print("[2.din useri2.refacparola] utilizator a carui parola se modifica :", inreg.id, inreg.email, 
            inreg.parola, inreg.moment)  #pt test
    inreg.parola = hash (parolanoua.parola)  #cripteaza cimpul parola cu o functie de tip hash,  modificare
                                        #cimp parola utilizator
    inreg.moment = datetime.now()   #actualizare data                                        
    print("[3.din useri2.refacparola] inregistrarea cu noua parola criptata :", inreg.id, inreg.email, 
     inreg.parola, inreg.moment)  #pt test
    db.add(inreg)   #modificare inreg in memo
    db.commit()     #inregistrare pe disc
    db.refresh(inreg)   #refacere info pe discuri (de ce?)
    return inreg    # FastAPI stie sa faca lista dintr-o inreg. filtrata din DB

#Daca se apeleaza in navigator=client cu: http://127.0.0.1:8000/postari/3
#   si body apel: {"titlu": "Titlul nou","continut": ["linia 1","linia 2","sfirsit"]}
# clientul primeste:
#   ["Mesaj de la server: articolul cu id",3,"a fost modificat in",{"titlu":"Titlul nou",
#   "ciorna":true,"id":3,"continut":"{\"linia 1\",\"linia 2\",sfirsit}","apreciere":null}]
#   cu starea: 200 Ok Standard response for successful HTTP requests. The actual response 
#   will depend on the request method used. In a GET request, the response will contain 
#   an entity corresponding to the requested resource. In a POST request the response will 
#   contain an entity describing or containing the result of the action
#Daca se apeleaza in navigator=client cu: http://127.0.0.1:8000/postari/44
#   si body apel: {"titlu": "Titlul nou","continut": ["linia 1","linia 2","sfirsit"]}
# clientul primeste:
#  {"detail":"Mesaj de la server: articolul cu id: 1 nu se gaseste in BD"}
#   cu starea: 404 Not Found The requested resource could not be found but may be 
#   available again in the future. Subsequent requests by the client are permissible
#Daca se apeleaza in navigator=client cu: http://127.0.0.1:8000/postari/sd
#   si body apel: {"titlu": "Titlul nou","continut": ["linia 1","linia 2","sfirsit"]}
# clientul primeste:
#   {"detail":[{"type":"int_parsing","loc":["path","id"],"msg":"Input should be a valid 
#   integer, unable to parse string as an integer","input":"sd",
#   "url":"https://errors.pydantic.dev/2.5/v/int_parsing"}]}
#   cu starea: 422 Unprocessable Entity The request was well-formed but was unable 
#   to be followed due to semantic errors    
#Daca se apeleaza in navigator=client cu: http://127.0.0.1:8000/postari/sd
#   si body apel: {"titlu": "Titlul nou ceva mai lung decit e admis","continut": 
#   ["linia 1","linia 2","sfirsit"]}
# clientul primeste:
#   {"detail":[{"type":"string_too_long","loc":["body","titlu"],
#   "msg":"String should have at most 23 characters",
#   "input":"Titlul  nou ceva mai lung decit admis","ctx":{"max_length":23},
#   "url":"https://errors.pydantic.dev/2.5/v/string_too_long"}]}
#   cu starea: 422 Unprocessable Entity The request was well-formed but was unable 
#   to be followed due to semantic errors