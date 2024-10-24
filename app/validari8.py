'''
Nume fisier:
    FastAPI\app\validari8.py

Autor
    Adrian Popescu

Proiect
    management de documente cu Python prin FastAPI
Implementeaza
    FastAPI Votes Route file: Part #84 Python API Course de Sanjeev Thiyagarajan
    FastAPI SQL Joins/ SQLAlchemy file: Part #86 Python API Course de Sanjeev Thiyagarajan

Scop
    pentru operatiunile de verificare a datelor primite de la client

Versiune anterioara
    FastAPI\app\validari6.py
    introduce relatiile intre cimpuri din clase SQLAlchemy diferite

nou:
    functiile de verificare a datelor privind votarea
'''
#
#   Modulul pentru validarea datelor de trimis si de filtrare a datelor primite
#   la server la BD PostgreSQL (Modele de date, scheme Pydantic)
#
#   ofera flexibilitate in definitiile claselor de validari astfel incit  validarile sa
#      fie diferite functie de operatiile CRUD dorite!!
#
# legatura intre baza de date si modelul datelor continute se face in main11.py!
#

from typing import List
from typing import Optional #defineste cimpuri otionale in structuri de date
from pydantic import BaseModel   #creaza tipologii de date deci include validari = scheme de date
from pydantic import Field  #clasa Field contine metadate si reguli de validare ale atributelor
            # modelului; e practic definitia coloanelor din modelele de date structurate tabelar
from pydantic import EmailStr #defineste validarea adreselor email
from typing_extensions import Annotated #pregatire pt date particulare


#
#   SECTIUNEA   Date Binare, date structurate, ... sint obiecte ale clasei BaseModel,
#
#clasa articolelor ce vor fi 'publicate pe sait' = primite prin interfata
#   operatiile FastAPI face apel la ea pentru a verif datelor trimise de client
#

#
# clase pentru verificarea datelor primite de la client
#

class ArticolBaza(BaseModel):  #se bazeaza pe clasa modelelor de date de baza 
             #din clasele pydantic, folosita ca baza a definitiilor claselor de lucru
    id: Optional[int] = None      #identificator unic al articolului, cheie de acces la articol
    titlu: str = Field (None, title="numele articolului", max_length=23 ) #metadata
    ciorna: bool=True   #cimp optional!!, semnifica implicit "articol nepublicabil", 
    continut: List[str] = []  #continutul propriu-zis al articolului    
    apreciere: Optional[int] = None #cimp optional, tip int, def in biblio typing
    idproprietar: Optional[int] = None     #cheie in tabela users a BD, coloana id tip int

class CreArticol(ArticolBaza):  #clasa de lucru pentru crearea de articole
            # ar trebui sa se bazeze pe clasa definita exhaustiv ArticolBaza
            # daca CreArticol de tip ArticolBaza, asteapta in intrare id 
            # si idproprietar pt posts, ceea ce nu-i bine !!!
    class Config:           #clasa necesara pentru conversia din SQLAlchemy in Pydantic
        from_attributes = True     #a.i. sa permita filtrarea; altfel eroare la executie ~non

class ModifArticol(ArticolBaza):  #clasa de lucru pentru a modifica articole existente
            # se bazeaza pe clasa definita exhaustiv ArticolBaza
            #ideea e buna, de vazut ce inseamna in practica functie de nevoi
            ## !!! Ceva nu merge aici !!
    class Config:           #clasa necesara pentru conversia din SQLAlchemy in Pydantic
        from_attributes = True     #a.i. sa permita filtrarea; altfel eroare la executie ~non

class UserBaza(BaseModel):  #se bazeaza pe clasa modelelor de date de baza 
             #din clasele pydantic, folosita ca baza a definitiilor claselor de lucru
    id: int     #identificator unic al utilizatortului, cheie de acces la user
    email: EmailStr # metadata folosita aici ca nume utilizator
    parola: str #metadata
    #ciorna: bool=True   #cimp optional!!, semnifica implicit "articol nepublicabil", 
    #continut: List[str] = []  #continutul propriu-zis al articolului    
    #apreciere: Optional[int] = None #cimp optional, tip int, def in biblio typing

class UserLogin(BaseModel): #definitia structurii datelor de la client pt login
    #generat dupa modelul definitiei clasei UserBaza
    email: EmailStr # metadata folosita aici ca nume utilizator
    parola: str #metadata

# verificary legate de jetoanele pentru autentificare

class Jeton(BaseModel): #structura de date de la client pentru token-ele de acces
    jeton: str      # corpul jetonului trimis de client
    tipjeton: str   # modul de lucru pentru prezentarea drepturilor de acces
                    # tipjeton = "bearer" => mesajul purtator al cererii de date
                    #       contine si jetonul de acces == jeton la purtator

class DateJeton(BaseModel):  #structura corpului jetonului trimis de client
    id: Optional[str] = None    #ar trebui sa nu fie optional, deocamdata ca demo!
        # dar ce-i cu timpul? prin oauth21.crearejetonacces la id am adaugat durata! 



#clase pentru filtrarea raspunsului serverului catre client

class FiltruUser(BaseModel):   #se bazeaza pe clasa modelelor de date de baza 
        #din clasele pydantic, folosita ca baza a definitiilor claselor de lucru
    id: int     #identificator unic al articolului, cheie de acces la utilizator (user)
    email: EmailStr
    #parola: str 
    moment: str   
    #filtreaza id, ciorna si apreciere
    class Config:           #clasa necesara pentru conversia din SQLAlchemy in Pydantic
        from_attributes = True     #a.i. sa permita filtrarea; altfel eroare la executie ~non

class CreUser(BaseModel):  #clasa pentru crearea de utilizatori
    email: EmailStr #obiect standard in pydantic
    parola: str #atentie, astfel se accepta parola nula!! tre puse conditii !!
    class Config:           #clasa necesara pentru conversia din SQLAlchemy in Pydantic
        from_attributes = True     #a.i. sa permita filtrarea; altfel eroare la executie ~non

class ModifNume(BaseModel):  #clasa pentru modificare nume de utilizator
    email: EmailStr #obiect standard in pydantic
    class Config:           #clasa necesara pentru conversia din SQLAlchemy in Pydantic
        from_attributes = True     #a.i. sa permita filtrarea; altfel eroare la executie ~non        

class ModifParola(BaseModel):  #clasa pentru modificare parola utilizator
    parola: str #atentie, astfel se accepta parola nula!! tre puse conditii !!
    class Config:           #clasa necesara pentru conversia din SQLAlchemy in Pydantic
        from_attributes = True     #a.i. sa permita filtrarea; altfel eroare la executie ~non        


#class FiltruArticol(ArticolBaza):  #Total timpit, nu inteleg de ce NU FILTREAZA!! 
class FiltruArticol(BaseModel):  #se bazeaza pe clasa modelelor de date de baza 
        #din clasele pydantic, folosita ca baza a definitiilor claselor de lucru
        #filtreaza id, ciorna, apreciere si idproprietar
    #id: int     #identificator unic al articolului, cheie de acces la articol
    titlu: str
    #ciorna: bool 
    continut:  str
    #apreciere: int
    #idproprietar: int 
    proprietar: FiltruUser  #introdus pentru corelarea cu relationarea clasei Post cu User
                    # definita in modele4.py

    class Config:           #clasa necesara pentru conversia din SQLAlchemy in Pydantic
        from_attributes = True     #a.i. sa permita filtrarea; altfel eroare la executie ~non

sensvot = Annotated[int, Field(le=1)] #definire lista valori acceptabile pentru valoarea votului
class CreVot(BaseModel):    #verifica sintaxa pt id articol si sens vot
    idart : int #conform definitiei id articol
    sens : sensvot #valorile permise pentru sensul votului (0 sterge votul atribuit anterior
                    # de utilizator, 1 adauga un vot celor date anterior de alti utilizatori)

class FiltruArticolCuVot(BaseModel):  #se bazeaza pe clasa modelelor de date de baza 
    Post:   FiltruArticol   #subtiata cu clasa articolelor trimise catre client
    voturi: int         #la care se adauga cimpul voturi

