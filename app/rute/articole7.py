'''
Nume fisier:
    FastAPI\app\rute\articole7.py

Autor
    Adrian Popescu

Proiect
    management de documente cu Python prin FastAPI
Implementeaza:
    FastAPI Votes/like Theory file: Part #81 Python API Course de Sanjeev Thiyagarajan
    FastAPI Creating Votes Table pgadmin file: Part #82 Python API Course de Sanjeev Thiyagarajan
    FastAPI Votes SQLAlchemy file: Part #83 Python API Course de Sanjeev Thiyagarajan
    FastAPI Votes Route file: Part #84 Python API Course de Sanjeev Thiyagarajan
    FastAPI SQL Joins/ SQLAlchemy file: Part #86 Python API Course de Sanjeev Thiyagarajan
    FastAPI Get One Post Join file: Part #87 Python API Course de Sanjeev Thiyagarajan


Versiune anterioara
    FastAPI\app\rute\articole6.py
nou: votarea:
        foloseste relatiile intre tabele (id utilizator cheie straina) pentru 
        rolurilor utiliatorilor (rindurile pot fi operate numai de anumiti utilizatori)
        foloseste modele6.py, relatia id user - document (articol de publicat)
    si afisarea votului prin folosirea SQL JOIN    
'''

from fastapi import Response #biblio pentru interpretare stari http ale serverului
from fastapi import status #biblio pentru codurile standard http ale serverului, folosit cu HTTPException
from fastapi import HTTPException #trateaza semnalele de eroare http, ! in loc de Response + status
from fastapi import Depends #trateaza conexiunile cu sesiunea de lucru cu DB prin ORM
## !! NOU APIRouter din fastapi
## !!!! Se va inlocui obiectul app definit in main.py cu un obiect local de tip ruter
from fastapi import APIRouter #pt rutele de acces la resurse, necesar pt separare user si articol

from typing import List #transforma in liste obiecte exprimate ca in BD
from typing import Optional #introduce variabile optionale

from sqlalchemy.orm import Session  #preia definitia sesiunii pe o BD din ORM-ul SQLAlchemy
from sqlalchemy import func #preia functii diverse precum COUNT

from validari8 import CreArticol, FiltruArticol, FiltruArticolCuVot, ModifArticol
    #preia definitia modelelor de date (schemelor de validare) din validari5.py
from bazadedate1 import get_db  #importa din bazadedate.py metoda de open/close DB session
from modele6 import Post,Vot  #preia definitia modelelor de date din modele4.py
from oauth26 import iausercurent  #preia metoda idutilizator din oauth21.py 

#s-a inlocuit din v9 obiectul app de tip FastAPI din main.py cu un obiect de acelasi tip apelabil
#  dintr-o pozitie superioara a ierarhiei de fisiere (module py)
#   ruter = APIRouter()    # NU se apeleaza main.app  !!    #introdus in main9.py
ruter = APIRouter(    #  introdus in v10 pentru limpezirea documentatiei
            prefix= "/postari",      #scurtata denumirea caii de acces inlocuid /postari cu /
            tags= ['Articole (postari)'])     #marcata gruparea cailor catre articole

# 1. Citeste intregul continut al BD Folosind ORM SQLAlchemy => db:Session = Depends(get_db)
#       este vorba despre tabela obiectul Post !!
#   Read    -> GET          /       @ruter.get("/numepagina")
#
#@ruter.get("/")  #metoda get = preia toate datele
#@ruter.get("/", response_model= List[FiltruArticol])  #metoda get = preia toate datele
@ruter.get("/", response_model= List[FiltruArticolCuVot])  #metoda get = preia toate datele
#async def iadinposts(db:Session = Depends(get_db), usercurent: int = Depends (iausercurent)): 
async def iadinposts(db:Session = Depends(get_db), usercurent: int = Depends (iausercurent),
                     limit: int = 10, skip: int =0, search: Optional[str] =""): 
        #functia intoarce toate rindurile tabelei deschise si inchise cu get_db
        # List transforma obiectul BD intr-o lista ce se poate trimite
        # FiltruArticol nu merge, nu filtreaza; mai mult, genereaza eroare la cimp nul in BD
    #interogheaza in modelul de date Post din modele4.py adica din tabela posts a BD, in 
    # sesiunea creata de Depends(get_db):
    # variabila limit este folosita ca modul al articolelor intoarse clientului
    # variabila skip este folosita ca pas al iqnorarii articolelor intoarse clientului
    #sqlinreg = db.query(Post)   #pregatire SQL regasire inregistrari
    #sqlinreg = db.query(Post).limit(limit)  #pregatire SQL regasire inregistrari in limita 
        # a maximum limit articole
    #sqlinreg = db.query(Post).limit(limit).offset(skip)  #pregatire SQL regasire inregistrari 
        # in limita a maximum limit articole, sarind primele skip articole intoarse de BD
    ##sqlinreg = db.query(Post).filter(Post.titlu.contains(search)).limit(limit).offset(skip)
    ##pregatire SQL pt regasire articole care contin sirul cu valoarea lui search in titlu
    ## in limita a maximum limit articole, sarind primele skip articole intoarse de BD
    
    #sqlinreg = db.query(Vot).filter(Vot.iduser == usercurent and Vot.idart == 4) #!! Nu filtreaza!!
    #sqlinreg = db.query(Vot).filter(Vot.idart == 4 and Vot.iduser == usercurent ) #!! FILTREAZA !!

    sqlinregcuvot = db.query(Post, func.count(Vot.idart).label("voturi")).join(Vot, 
        Vot.idart==Post.id, isouter=True).group_by(Post.id).filter(Post.titlu.contains(
            search)).limit(limit).offset(skip) #adauga date din voturi     
    #print ("[Articole7] 0. sqlinregcuvot =", sqlinregcuvot)
    inreg = db.execute(sqlinregcuvot).mappings().all()   #executie SQL pregatit mai sus, 
        #cu intoarcerea tuturor rindurilor

    #sqlinreg = db.query(Post).filter(Post.idproprietar == usercurent) 
     #print ("[Articole7] 1. sqlinreg =", sqlinregcuvot)
    
    #pregatire SQL pt regasirea tuturor articolelor si cu numararea voturilor pentru fiecare
    #inreg = sqlinreg.all()    #executie SQL cu intoarcerea tuturor rindurilor tabelei
    #    inreg = sqlinreg.filter(Post.idproprietar == usercurent).all()    #executie SQL cu intoarcerea 
        # rindurilor tabelei care au valoarea coloanei idproprietar egala cu valoarea usercurent
    #print ("[Articole7] 2.Sint serverul, inreg = ", inreg)
    #return {"Sint serverul, rindurile tabelei sint": inreg}  
            # FastAPI serializeaza automat si transforma in JSON
    return inreg  #zice ca raspunsul este mai curat astfel
    # Atentie, FastAPI nu stie sa faca lista din toate cele filtrate din DB, trebuie
    #   folosita transformarea explicita cu List
'''
Se apeleaza in navigator=client cu:  http://127.0.0.1:8000/postari
Intoarce:
    [{"Post":{"titlu":"Articol nou","continut":"{\"Continut nou\",sfirsit}",
    "proprietar":{"id":48,"email":"eu@eu.eu","moment":"time.struct_time(tm_year=2024, tm_mon=5, 
    tm_mday=20, tm_hour=18, tm_min=5, tm_sec=52, tm_wday=0, tm_yday=141, tm_isdst=1)"}},"voturi":1},
    {"Post":{"titlu":"Articol nou","continut":"{\"Continut nou\",sfirsit}",
    "proprietar":{"id":48,"email":"eu@eu.eu","moment":"time.struct_time(tm_year=2024, tm_mon=5,
      tm_mday=20, tm_hour=18, tm_min=5, tm_sec=52, tm_wday=0, tm_yday=141, tm_isdst=1)"}},"voturi":0}

In continuare punctele 2., 3.,...
exemple de primire de date de la client cu validare (de fapt transformare intr-o
structura predefinita pe server; folosita biblioteca Pydantic (BaseModel si Fields)
Structura dorita este cea de mai sus, definita in obiectul FiltruArticolCuVot":
    id cheie de acces la articol, titlu cu structura de cimp (cap de coloana de 
        tabela de date structurate), stare dorita (optional, implicit ciorna nepublicabila) 
        si continut propriu-zis, definite astfel:
    id: int     #identificator unic al articolului, 
    titlu: str = Field (None, title="numele articolului", max_length=23)
    ciorna: bool=True 
    continut: List[str] = []  #continutul propriu-zis al articolului
    etc.
'''

#
#  ZONA   Manipularea datelor pe server cu tratarea "exceptiilor" 
#              

# 2. Creaza (="publica art. nou" pe sait) inregistrind in BD PostgreSQL cu ORM-ul SQLAlchemy
#
@ruter.post("/", status_code= status.HTTP_201_CREATED, response_model=FiltruArticol)
                #si filtreaza raspunsul catre client
async def creazainBD(inreg:CreArticol, db:Session = Depends(get_db),
    usercurent: int = Depends (iausercurent)): # introdusa nou fata de vers. precedenta
    #inreg = Post(titlu=inreg.titlu, ciorna=inreg.ciorna, continut=inreg.continut,
    #                     apreciere=inreg.apreciere)
    #print("Utilizator curent este: ", usercurent.__dict__)   #pentru test
    ## cu main12.py si validari5.py, nu asteapta in intrare cimpurile id si idproprietar
    inreg.idproprietar=usercurent
    inreg = Post (**inreg.dict()) #excelent, sintaxa speciala echivalenta!!
        #a transformat in dictionar, apoi a despachetat dictionarul
    db.add(inreg)   #adaugat la in RAM
    db.commit()     #inscris pe disc
    db.refresh(inreg)       #improspatat a.i. noua inreg sa fie vizibila
    #return {"Sint serverul; in BD s-a inregistrat": inreg}
    return inreg   #zice ca raspunsul este mai curat astfel
        #merge asa fiindca FastAPI stie sa transforme acest obiect intr-unul de tip lista
'''
Daca clientul cu:     http://127.0.0.1:8000/postari/
trimite: {"titlu": "Saispce","continut": ["linia 1","sfirsit"]}
serverul il accepta cu numele intern inreg de tip Articol si cu:
    return {"Sint serverul; in BD s-a inregistrat": inreg}
intoarce: {"Sint serverul; in BD s-a inregistrat":{"apreciere":null,
    "continut":"{\"linia 1\",sfirsit}","titlu":"Saispce","ciorna":true,"id":9}}
cu starea: 201 Created 
The request has been fulfilled and resulted in a new resource being created

nu o inteleg de ce "eroare interna" daca lipseste "titlu" in corpul cererii clientului
 nu nu se semnaleaza clientului eroare de sintaxa!!!!!!                               
'''


# 3. Citeste rindul (articolul) cu identif id din BD folosind ORM SQLAlchemy
#   Read    -> GET          /       @ruter.get("/ceva/{parametru}")
@ruter.get("/{id}", response_model= FiltruArticol)  
#@ruter.get("/{id}")#, response_model= FiltruArticolCuVot)  #nu reusesc sa adaug voturile!!
# metoda get = intoarce clientului art cu id cerut, filtrat
async def iaarticol(id:int, db:Session = Depends(get_db), 
                usercurent: int = Depends (iausercurent)): #vede id, trimite date si stari
    #inreg = db.query(Post).filter(Post.id == id).first()  #cauta in tabela posts a BD, in
            # sesiunea deschisa pe BD prin metoda get_db, prima intilnire a inreg id
            # fiindca id e unic, nu cauti mai departe (=all) ci opresti cautarea (<=first)
    #inregSQL= db.query(Post, func.count(Vot.idart)).join(Vot, Vot.idart==Post.id, 
     #           isouter=True).group_by(Post.id).filter(Post.id == id)
#    inreg = db.query(Post, func.count(Vot.idart)).join(Vot, Vot.idart==Post.id, isouter=True).group_by(
#                Post.id).filter(Post.id == id).first()  #cauta in tabela posts a BD, in
    #inreg = db.execute(inregSQL).mappings().first()   #executie SQL pregatit mai sus, 

    inreg = db.query(Post).filter(Post.id == id)
    print(inreg)
    #inreg = db.execute(inreg).mappings().first() #genereaza o eroare!!
    inreg = inreg.first()       #functioneaza corect!!
    print("inreg = ", inreg)

    if inreg == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                detail = f"Mesaj de la server: articolul cu id: {id} nu se gaseste in BD")
    #if inreg.idproprietar != usercurent:    #verifica dreptul de acces
    #    raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, 
    #            detail = f"Mesaj de la server: actiune neautorizata")                    
    #return ("Sint serverul; articolul cu id", id, "in BD este:", inreg) #intoarce eroare
    #zice ca raspunsul este mai curat astfel
    return inreg    # FastAPI stie sa faca lista dintr-o inreg. filtrata din DB
                    #cum este de ex <modele6.Post object at 0x0000024291E8A110>
#Apelat in navigator=client cu: http://127.0.0.1:8000/postari/4
#   Intoarce: {"titlu":"Articol secund","continut":"{\"Continut nou\",sfirsit}",
#       "proprietar":{"id":48,"email":"eu@eu.eu","moment":"time.struct_time(tm_year=2024, 
#           tm_mon=5, tm_mday=20, tm_hour=18, tm_min=5, tm_sec=52, tm_wday=0, tm_yday=141, 
#           tm_isdst=1)"}}
#   cu starea: 200 Ok Standard response for successful HTTP requests. The actual response 
#   will depend on the request method used. In a GET request, the response will contain 
#   an entity corresponding to the requested resource. In a POST request the response will 
#   contain an entity describing or containing the result of the action
#Apelat in navigator=client cu: http://127.0.0.1:8000/postari/101
#   Intoarce: {"detail":"Mesaj de la server: articolul cu id: 2002 nu se gaseste in BD"}
#   cu starea: 404 Not Found  The requested resource could not be found but may be available
#    again in the future. Subsequent requests by the client are permissible.
#Apelat in navigator=client cu: http://127.0.0.1:8000/postari/unu
#   Intoarce: {"detail":[{"type":"int_parsing","loc":["path","id"],
#   "msg":"Input should be a valid integer, unable to parse string as an integer",
#   "input":"unu","url":"https://errors.pydantic.dev/2.5/v/int_parsing"}]}
#   cu starea: 422 Unprocessable Entity The request was well-formed but was unable 
#   to be followed due to semantic errors    
    

# 4. Sterge anumite date din BD PostgreSQL de pe server, un articol cu identificatorul id
#  Delete  -> DELETE    /articole/:id   @ruter.delete("/articole/{id}")
#
@ruter.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT) #HTTP_204_NO_CONTENT
# == The server successfully processed the request, but is not returning any content
async def stergart(id:int, db:Session = Depends(get_db), 
                   usercurent: int = Depends (iausercurent)):     # sterge inregistrari
    sqlinreg = db.query(Post).filter(Post.id == id)  #pregateste cautarea in tabela posts
            # a BD in sesiunea deschisa pe BD prin metoda get_db (doar genereaza cod SQL,  
            # nu executa si cautarea propriu-zisa!)
    inreg = sqlinreg.first()  #cauta prima aparitie a inreg cf. sql pregatit in sqlinreg
    # fiindca id e unic, nu cautam mai departe (=all) ci oprim cautarea (<=first)
    #print(" in articole 3 rind 172 inreg.idproprietar: ", inreg.idproprietar) #pt test
    if inreg == None: #verifica existenta inregistrarii
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                detail = f"Mesaj de la server: articolul cu id: {id} nu se gaseste in BD")
    if inreg.idproprietar != usercurent:    #verifica dreptul de acces
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, 
                detail = f"Mesaj de la server: actiune neautorizata")                    
    sqlinreg.delete(synchronize_session=False)  #stergere in memo
    db.commit()   # inscrie pe discuri
    return Response(status_code=status.HTTP_204_NO_CONTENT) #conform standardului http
#       pentru DELETE sa nu trimiti indarat date DELOC !!!
#Se apeleaza in navigator=client cu: http://127.0.0.1:8000/postari/1 # daca inreg cu id=1 exista
# clientul primeste:
#
#   cu starea: 204 No Content The server successfully processed the request, 
#   but is not returning any content
#Se apeleaza in navigator=client cu: http://127.0.0.1:8000/postari/1 # daca inreg cu id=1 NU exista
# clientul primeste:
#  {"detail": "Mesaj de la server: articolul cu id: 67 nu se gaseste in BD"}
#   cu starea: 404 Not Found The requested resource could not be found but may be 
#   available again in the future. Subsequent requests by the client are permissible    
#Se apeleaza in navigator=client cu: http://127.0.0.1:8000/postari/67df
#   Intoarce: {"detail":[{"type":"int_parsing","loc":["path","id"],
#   "msg":"Input should be a valid integer, unable to parse string as an integer",
#   "input":"unu","url":"https://errors.pydantic.dev/2.5/v/int_parsing"}]}
#   cu starea: 422 Unprocessable Entity The request was well-formed but was unable 
#   to be followed due to semantic errors    


#
# 5. Actualizeaza anumite date in BD pe server, in parte sau in totalitate un 
#                                                articol cu identificatorul id
#  Update  -> PUT    /articole/:id   @ruter.put("/articole/{id}")
#   atentie, trebuie pastrate valorile anterioare, de verif pt. toate cimpurile!!
@ruter.put("/{id}", status_code= status.HTTP_200_OK, response_model= FiltruArticol) 
async def refac(id:int, numenou:ModifArticol, db:Session = Depends(get_db),
                usercurent: int = Depends (iausercurent)):  
# functia modifica articolul cu id !! IN INTREGIME => pt. modif. partiala tre. rescris !!
# prin nume:Articol se folosesc functiile de verificare a datelor primite in nume
    sqlinreg = db.query(Post).filter(Post.id == id)  #pregateste cautarea in tabela posts a BD,
            # a BD in sesiunea deschisa pe BD prin metoda get_db (doar genereaza cod SQL,  
            # nu executa si cautarea propriu-zisa!)
    inreg = sqlinreg.first()    # se pare ca acum cauta prima intilnire a inreg id
            # fiindca id e unic, nu cautam mai departe (=all) ci oprim cautarea (<=first)
    if inreg == None:   #verifica existenta inregistrarii
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                detail = f"Mesaj de la server: articolul cu id: {id} nu se gaseste in BD")
    if inreg.idproprietar != usercurent:    #verifica dreptul de acces la inregistrare
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, 
                detail = f"Mesaj de la server: actiune neautorizata")                    
    numenou.id = id     #atentie, este cimp obligatoriu in BD, tre' pastrat/refacut!!
    numenou.idproprietar=usercurent #atentie, este cimp obligatoriu in BD, tre' pastrat/refacut!!
    sqlinreg.update(numenou.dict(), synchronize_session=False)
    #print("2.inreg.idproprietar din articole3.refac:",numenou.idproprietar) #pt test
    db.commit()
    #print("3.inreg.idproprietar din articole3.refac:", inreg.idproprietar)   ##pt.test
    # return ("Mesaj de la server: articolul cu id", id, "a fost modificat in", sqlinreg.first())
    return sqlinreg.first()    #zice ca raspunsul este mai curat
        #pe de alta parte, FastAPI are grija sa transforme iesirea intr-o lista
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