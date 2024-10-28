'''
Fisier:
    FastAPI/app/autentif4.py

Autor:
    Adrian Popescu

Proiect
    management de documente cu Python prin FastAPI

Implementeaza:
    FastAPI Environment Variables.py file: Part #80 Python API Course de Sanjeev Thiyagarajan   
    FastAPI Vote/Like theory: Part #81 Python API Course de Sanjeev Thiyagarajan
    FastAPI Creating Votes Table pgadmin file: Part #82 Python API Course de Sanjeev Thiyagarajan
    FastAPI Votes SQLAlchemy file: Part #83 Python API Course de Sanjeev Thiyagarajan
    FastAPI Votes Route file: Part #84 Python API Course de Sanjeev Thiyagarajan    
    FastAPI SQL Joins/ SQLAlchemy file: Part #86 Python API Course de Sanjeev Thiyagarajan

Scop:
    verificarea autenticitatii credentialelor utilizatorilor

Versiune anterioara:
    FastAPI/app/autentif2.py

Nou:
    votarea <= foloseste modele6.py
'''

from fastapi import APIRouter
from fastapi import Depends #trateaza conexiunile cu sesiunea de lucru cu DB prin ORM
from ..bazadedate1 import get_db  #importa din bazadedate.py metoda de open/close DB session
from sqlalchemy.orm import Session  #preia definitia sesiunii pe o BD din ORM-ul SQLAlchemy
from fastapi import HTTPException #trateaza semnalele de eroare http, ! in loc de Response + status
from fastapi import status #biblio pentru codurile standard http ale serverului, folosit cu HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm   #introduce formular standard pt u + p, pt
        # a nu mai trimite credentialele ca rind (raw) JSON, ci tabelar (form)
        # totodata, cimpurile credentialelor se vor numai username si password, standard FastAPI !!

from modele6 import User  #definitia modelelui de date pentru User din modele4.py
from validari8 import UserLogin
from util1 import compara   #preia definitia pentru verificarea hash parola
from oauth26 import crearejetonacces   #modulul pentru manipularea jetoanelor de acces

ruter = APIRouter(
            tags= ['Autentificare'])  #grupate metodele pt autentificarea cererilor clientilor

#primeste credentiale, le verifica, daca Ok creaza si trimite token cu id si momentul expirarii
@ruter.post("/login")
#async def login(credentiale:UserLogin, db:Session = Depends(get_db)): #valabil in main10.py
#inreg = db.query(User).filter(User.email == credentiale.email).first()  #cauta in tabela users a BD
#in aceasta versiune credentialele se tot trimit prin corpul cererii dar nu ca rind JSON (ca mai 
# sus in comentarii) ci ca date sub forma de tabel => apelul nu mai este JSON raw ci tabel!!
async def login(credentiale:OAuth2PasswordRequestForm = Depends(), 
                db:Session = Depends(get_db)):  #trateaza credentiale ca o inreg in BD
    #cauta in BD inregistrarea potrivita, dupa numele de utilizator indicat de client
    #primeste un dictionar {"username":"uytiu", "password":"bla876ytr"}
    inreg = db.query(User).filter(User.email == credentiale.username).first()  #cauta in tabela users a BD,
            # in sesiunea deschisa pe BD prin metoda get_db, prima intilnire a inreg credentiale.username
            # fiindca e unic, nu cauti mai departe (=all) ci opresti cautarea (<=first)
    #print ("Sint serverul, inreg este", inreg.email, inreg.parola)
    if inreg == None:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, 
                detail = f"Mesaj de la server: credentialele primite nu sint cunoscute")
                # buna practica => in raspuns nu dam indicatii despre ce-i prost, nume sau parola
    #compara(User.parola, inreg.parola)  #verifica corectitudinea parolei indicate de client
    #if not compara(credentiale.parola, inreg.parola):  #valabil in versiunea anterioara cu raw JSON
    if not compara(credentiale.password, inreg.parola):  #valabil in versiunea anterioara cu raw JSON
    # if not compara(User.parola, inreg.parola):  #verifica corectitudinea parolei indicate de client
        # if not compara(User.parola, inreg.parola):  #verifica corectitudinea parolei indicate de client
        # buna practica => in raspuns nu dam indicatii despre ce-i prost, nume sau parola
        # poate asa este mai clar apelul, nu confundam cu alte metode de comparare
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, 
                detail = f"Mesaj de la server: credentialele primite nu sint cunoscute")
    #creare jeton (= mesaj continind credentialele criptate si durata valabilitatii mesajului)
    #   metoda oauth21.crearejetonacces primeste id-ul din BD si adauga durata valabilitatii,
    #       algoritmul si cheia de criptare al jetonului (astea-s constante in metoda!)
    jetonacces=crearejetonacces(date={"idutilizator":inreg.id}) #intoarce jetonul
    #return {"Jeton": "exemplu de token (jeton=token)"}  #pentru facilitarea testarii metodei
    return {"jeton": jetonacces, "tipjeton":"bearer"}  #intoarce jetonul

'''
valabil din oauth2.py si main10.py, unde credentialele se primesc ca rind in corpul cererii
#Apelat in navigator=client cu: http://127.0.0.1:8000/login
# si body JSON {"email":"eu@mfinante.ro","parola": "parola321"}
# #   Intoarce: ["exemplu de token (jeton=token)","Jeton"]
#   cu starea: 200 Ok Standard response for successful HTTP requests. The actual response 
#   will depend on the request method used. In a GET request, the response will contain 
#   an entity corresponding to the requested resource. In a POST request the response will 
#   contain an entity describing or containing the result of the action
#Apelat in navigator=client cu: http://127.0.0.1:8000/users
# si body JSON {"email":"eu1@mfinante.ro","parola": "parola321"}
#           sau {"email":"eu@mfinante.ro","parola": "parola21"}
#   Intoarce: {"detail":"Mesaj de la server: credentialele primite nu sint cunoscute"}
#   cu starea: 404 Not Found  The requested resource could not be found but may be available
#    again in the future. Subsequent requests by the client are permissible.
#Apelat in navigator=client cu: http://127.0.0.1:8000/login
# si body JSON {"email":"eu1@mfinante.ro","parol": "parola321"}
#   Intoarce:{"detail":[{"type":"missing","loc":["body","parola"],"msg":"Field required",
#   "input":{"email":"eu@mfinante.ro","parol":"parola21"},
#   "url":"https://errors.pydantic.dev/2.5/v/missing"}]}
# si body JSON {"email":"eu1mfinante.ro","parola": "parola321"}
#   Intoarce: {"detail":[{"type":"value_error","loc":["body","email"],"msg":"value is not a 
#       valid email address: The email address is not valid. It must have exactly 
#       one @-sign.","input":"eumfinante.ro","ctx":{"reason":"The email address is not valid.
#        It must have exactly one @-sign."}}]}

valabil din oauth2.py si main11.py, unde credentialele se primesc ca formular (form)
#Apelat in navigator=client cu: http://127.0.0.1:8000/login
# si body form-data key username, value text eu@mfinante.ro, key password, value text parola321
#   Intoarce: {"jeton":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZHV0aWxpemF0b3IiOjM1LCJleHBpcm
#   FsYSI6IjIwMjQtMDYtMTkgMTc6NDU6NDkuMTI2MDYxIn0.tJSeh2Q2R0f6SAjeekbjaoyGVJuknzxpHd4QgQ9TpfQ",
#   "tipjeton":"bearer"}
#   cu starea: 200 Ok Standard response for successful HTTP requests. The actual response 
#   will depend on the request method used. In a GET request, the response will contain 
#   an entity corresponding to the requested resource. In a POST request the response will 
#   contain an entity describing or containing the result of the action
#Apelat in navigator=client cu: http://127.0.0.1:8000/users
# si body form-data 
#       key username, value text eu1@mfinante.ro, key password, value text parola321
# sau   key username, value text eu@mfinante.ro, key password, value text parola21
#   Intoarce: {"detail":"Mesaj de la server: credentialele primite nu sint cunoscute"}
#   cu starea: 404 Not Found  The requested resource could not be found but may be available
#    again in the future. Subsequent requests by the client are permissible.
#Apelat in navigator=client cu: http://127.0.0.1:8000/login
# si body form-data 
#       key email value text eu1@mfinante.ro,key password value text parola321
#   Intoarce:{"detail":[{"type":"missing","loc":["body","username"],"msg":"Field required",
#       "input":null,"url":"https://errors.pydantic.dev/2.5/v/missing"}]},
# si body form-data 
#       key username value text eu@mfinante.ro,key parola value text parola321
#   Intoarce: {"detail":[{"type":"missing","loc":["body","password"],"msg":"Field required",
#       "input":null,"url":"https://errors.pydantic.dev/2.5/v/missing"}]}

'''