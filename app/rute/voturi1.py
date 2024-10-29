'''
Fisier:
    FastAPI/app/rute/voturi1.py

Autor:
    Adrian Popescu

Proiect
    management de documente cu Python prin FastAPI

Implementeaza:
    FastAPI Votes Route: Part #84 Python API Course de Sanjeev Thiyagarajan
    si
        FastAPI Votes Theory, Table, SQLALchemy, Route, Joins, Joins in SQLAlchemy,
        Get One with Joins: Part #8X Python API Course de Sanjeev Thiyagarajan
        FastAPI SQL Joins/ SQLAlchemy file: Part #86 Python API Course de Sanjeev Thiyagarajan
Scop:
    votarea articolelor
    Specificatii:   modul separat, calea de acces este: "/voturi"
                    id utilizator este extras din tokenul de acces JWT
                    corpul cererii contine id articol si sensul votului
                    sensul votului: 1 adauga vot pt articol, 0 elimina vot
                    un utilizator poate adauga vot o singura data pt un articol
                        adica un articol nu poate primi mai multe puncte de la
                        acelasi utilizator
Versiune anterioara:
    FastAPI/app/rute/voturi.py
'''

from fastapi import APIRouter
from fastapi import Depends #trateaza conexiunile cu sesiunea de lucru cu DB prin ORM
from sqlalchemy.orm import Session  #preia definitia sesiunii pe o BD din ORM-ul SQLAlchemy
from fastapi import HTTPException #trateaza semnalele de eroare http, ! in loc de Response + status
from fastapi import status #biblio pentru codurile standard http ale serverului, folosit cu HTTPException

from ..bazadedate1 import get_db  #importa din bazadedateX.py metoda de open/close DB session
from ..validari8 import CreVot #verificarea datelor de intrare pentru autentificare (=login)
from ..modele6 import Post, Vot   #verificarea datelor trimise de client pentru votare
from ..oauth26 import iausercurent   #modulul pentru manipularea jetoanelor de acces

ruter = APIRouter(
            prefix= "/voturi",    #scurtata denumirea caii de acces inlocuid /voturi cu /
            tags= ['Votare'])     #grupate metodele pt votarea articolelor

# 1. Creaza si modifica voturi (="voteaza" articole existente sait, operind pentru un 
#       utilizator existent, autentificat)
#   pentru autentificare foloseste datele primite prin jetonul de acces JWT bearer, pentru
#       actualizare vot foloseste datele din corpul cererii de la client, actualizarile se
#       fac in tabela voturi a BD
#
@ruter.post("/", status_code= status.HTTP_201_CREATED)
async def voteaza(vot:CreVot, db:Session = Depends(get_db),
                    usercurent: int = Depends (iausercurent)):
    print("1.[voturi.py] utilizator:", usercurent, "articol votat:",vot.idart, "vot:", vot.sens) #pt test
    #verifica in tabela posts a BD daca existenta articolului
    cautarticol = db.query(Post).filter(Post. id == vot.idart) 
    articolgasit = cautarticol.first()
    if not articolgasit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail= f"articol {vot.idart} inexistent")
    #verifica in tabela voturi daca articolul a mai fost votat de utilizator
    cautvot = db.query(Vot).filter(Vot.iduser == usercurent, Vot.idart == vot.idart)
    votgasit = cautvot.first()
    #print("2.[voturi.py] gasit in BD un vot similar:", votgasit) #pt test
    if  vot.sens == 1:   #adaugare vot
        if votgasit:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail= f"articol {vot.idart} deja votat de {usercurent}")
        else:
            votnou = Vot(idart = vot.idart, iduser = usercurent)   #creaza integ pentru votare
            db.add(votnou)
            db.commit()
            return ("Mesaj de la server: votul a fost inregistrat")
    else:
        if not votgasit:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail= f"articolul {vot.idart} nu a fost votat de {usercurent}")
        cautvot.delete(synchronize_session=False)
        db.commit()
        return ("Mesaj de la server: votul a fost sters")