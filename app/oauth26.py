'''
Fisier:
    FastAPI/app/oauth26.py

Autor:
    Adrian Popescu

Proiect
    management de documente cu Python prin FastAPI

Implementeaza 
    FastAPI Environment Variables: Part #80 Python API Course dr Sanjeev Thiyagarajan
    FastAPI SQL Joins/ SQLAlchemy file: Part #86 Python API Course de Sanjeev Thiyagarajan

Scop:
    generarea JWT (jetoane JSON) si verificarea autenticitatii acestora

Versiune anterioara:
        FastAPI\app\rute\oauth24.py
    nou:
    stabilirea variabilelor "de mediu" necesare in dezvoltarea si apoi exploatarea aplicatiei

'''

'''
Pentru crearea jetoanelor pentru securitate sint necesare trei elemente:
    algoritmul de criptare, cheia (cheia secreta = private key, in cazul algoritmilor asimetrici)
    si durata de valabilitate a jetonului (daca nu se indica, implicit, este perpetua)
In acest scop, trebuie instalata biblioteca pentru criptografie:
>pip install python-jose(cryptography)
'''

from jose import JOSEError, jwt #din biblioteca pentru semnarea si verificarea jetoanelor JSON
from datetime import datetime, timedelta    #metodele necesare pentru a cunoaste momentul si
        #   a stabili o perioada de timp

from fastapi import Depends, status, HTTPException  #necesare pt. creare punct final al caii de
    # de acces la login
from fastapi.security import OAuth2PasswordBearer   #acelasi scop
from sqlalchemy.orm import Session  #preia definitia sesiunii pe o BD din ORM-ul SQLAlchemy

from bazadedate1 import get_db  #importa din bazadedate.py metoda de open/close DB session
from modele6 import User  #preia definitia modelelor de date din modele4.py
from validari8 import DateJeton    #structura de date propriu-zise a jetonului
from config import mediu     #preia definitiile variabilelor de mediu

# CONSTANTE:    
#CHEIESECRETA     = "abcdef0816242539abcdef34269723765abcdef90814376543abcdef876236bd"
#   pentru a genera un astfel de sir (cod hexa) se poate folosi comanda:  openssl rand -hex 32
#   pentru a a da aceasta comanda, apelezi terminalul bash, pe linga cmd sau Python sau 
#   powershell din Microsoft Visio care vada prompterul $
#   CHEIESECRETA sta pe server!!
#ALGORITMCRIPTARE = "HS256"
#DURATAVALABILITATEJETON = 480  # UM = min

#variabilele mediului de lucru (= instalare si executie)
CHEIESECRETA     = mediu.cheiesecreta
ALGORITMCRIPTARE = mediu.algoritmcriptare
DURATAVALABILITATEJETON = mediu.duratavalabilitatejeton  # UM = min


#
#   Ori de cite ori, exista un punct final de acces (end point for a path operation) care 
# trebuie protejat, cum sint de exemplu ordinele de scriere, modificare sau stergere a unor
# date din BD, in functia de acces trebuie prevazuta o "dependinta" suplimentara, pentru a
# verifica legitimitatea operatiei => introduci dependenta
#   iaidutilizator: int = Depends (oauth2.crearejetonacces)
#   vezi articole2.py, operatia de adaugare articol in BD
oauthvalid = OAuth2PasswordBearer(tokenUrl='login')  #creat punctul final al caii de acces 
    # (path operation) a metodei login  #!! cimpul tokenUrl tre sa aiba valoarea data
    # de @ruter.post("/login") ...... async def login(credentiale:........ din autentif.py
    # oricare ar fi; aici este: login  (atentie, fara: / )

#
# Crearea jetonului tip OAuth2 pentru acces la interfete de aplicatii
# structura date de tip dictionar trebuie sa contina cimpurile necesare pentru identificarea
#   utilizatorului, a drepturilor sale de acces in amanunt, dupa cum vrei!!
#
def crearejetonacces (date:dict):   #extindere corp (body) JSON de tip jeton acces
    ptjeton={}
    ptjeton.update(date)   #in corpul jetonului se pune o copie a datelor de intrare
    expira = datetime.now() + timedelta(minutes=DURATAVALABILITATEJETON) #stabileste moment expirare
    expira=str(expira)
    ptjeton.update({"expirala":expira})   #corpul jetonului este un dictionar, cf. definitiei
        #momentul expirarii este adus la zi
    #ptjeton = {"idutilizator": 35,"expirala": expira}
    print("id: ", date, "   expirala: ", expira)     
    corpjeton=jwt.encode(ptjeton, key=CHEIESECRETA, algorithm='HS256')
    return corpjeton

#   Folosita de metoda iaiduitilizator pentru executarea ordinelor de lucru conform drepturilor
#    de acces ale utilizatorului; 

# Extrage jetonul de acces prezentat intrat prin jeton:str si, daca nu sint neconformitati, intoarce
#  datele extrase; orice neconformitate intrerupe executia normala a programului (main), serverul
#  generind catre client codul de eroare (normal in standard HTTPS) pe care aceasta rutina l-a 
#  primit prin variabila de intrare credentials_exception 
#
def verifjetonanacces (jeton: str, credentials_exception): #extrage jetonul din ordinele de acces
        # verifica daca jeton:str indeplineste conditiile stabilite pentru un jeton prin variabila
        # de intrare credentials_exception si intoarce jetonul sau semnaleaza exceptia de la reguli
    try:     #necesar try, fiindca nu vrei sa te impiedici daca verificarea descopera inconsistente
        corpjeton=jwt.decode(jeton, key=CHEIESECRETA, algorithms='HS256') #extrage corpul jetonului
        idextras: str = corpjeton.get("idutilizator") #extrage id-ul din corpul jetonului si il face str (daca nu este)
        expiralaextras = corpjeton.get("expirala") #extrage momentul expirarii
        # print("idextras: ", idextras, "  expiralaextras: ", expiralaextras) #pentru test
        if idextras is None:
            raise credentials_exception
        dtextras = datetime.strptime(expiralaextras, '%Y-%m-%d %H:%M:%S.%f')
        #print("dtextras: ", dtextras, "datetime.now(): ", datetime.now())  #pentru test
        if dtextras < datetime.now():
            raise credentials_exception
        datecorpjeton = DateJeton(id=str(idextras))   #aici acum id utilizator, se adauga mai multe cimpuri!!
    except JOSEError:           #orice erori vor aparea la verificare, vor fi semnalizate global
        raise credentials_exception
    return datecorpjeton    #daca jetonul este conform


#
# Lanseaza verificarea conformitatii jetoanelor de acces si, daca jetonul prezinta date conforme,
#  extrage din BD si intoarce datele relevante despre utilizator (pentru a insoti, pe parcursul 
#  executiei programului ordinele de lucru trimise de client catre server); indica totodata 
# rutinei de verificare sa intrerupa executia programului principal si tipul de eroare pe care 
# serverul il va genera in caz de neconformitate
#
def iausercurent(jeton: str = Depends(oauthvalid), db:Session = Depends(get_db)):    #intoarce
    # (extrage) id-ul din BD de utilizatori, sau alte date relevante despre utilizator si 
    # drepturile lui de acces si operare a datelor; cu alte cuvinte, extrage din BD datele necesare
    #  pentru a dovedi legitimitatea ordinelor de lucru; !! permite ca ordinele de lucru interne pe 
    # server sa fie insotite de info despre utilizatorii care le-au dat!!
    credentials_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,
            detail= f"Mesaj de la server: neautorizat",
            headers={"WWW-Authenticate":"Bearer"})
    #return verifjetonanacces(jeton, credentials_exception) #pentru test
    datedinjeton = verifjetonanacces(jeton, credentials_exception) # lanseaza verificare jeton 
        # si ia date din el
    usercurent = db.query(User).filter(User.id == datedinjeton.id).first()  #cauta in tabela users a BD, 
            # in sesiunea deschisa pe BD prin metoda get_db; la prima intilnire a inreg cu id
            # fiindca id e unic, nu cauti mai departe (<=all) ci opresti cautarea (<=first)
    #return usercurent  # intoarce intreaga inregistrare despre utilizatorul verificat si acceptat 
            # sa foloseasca serverul
    #l=usercurent.id    
    #print("l din oauth21.iausercurent:", l)
    return usercurent.id  # intoarce id al utilizatorului verificat si acceptat sa foloseasca serverul
    