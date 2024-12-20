'''
Nume fisier:
    FastAPI\app\__init__.py

Autor
    Adrian Popescu

Proiect
    management de documente cu Python prin FastAPI

Implementeaza
    FastAPI Cleanup main.py file: Part #79 Python API Course de Sanjeev Thiyagarajan

executat cu
    app>uvicorn main13:app --reload
    
structura de module (=fisiere) este

    FastAPI\app
        cu
            __init__.py     #de fata
            bazadedate.py
            main13.py
            modele4.py      #introduce relatiile intre tabele
            util1.py
            validari6.py    #introduce validarile pentru jetoane

    FastAPI\app\rute
        cu
            __init__.py     #gol
            articole3.py    #introduce accesul la scriere in BD, numai cu drept atribuit utilizatorului
            autentif1.py
            oauth22.py    #introduce validarea jetoanelor  
            useri2.py   


Implementeaza
    FastAPI Configurare cu date in fisiere externe Route file: Part #80 Python API Course de Sanjeev Thiyagarajan

executat cu
    app>uvicorn main14:app --reload
    
structura de module (=fisiere) este

    FastAPI
        cu
            mediudelucru.env     #creat cu main 14 pentru variabilele de mediu de lucru
            .gitignore  #creat cu main 14 pentru variabilele de mediu de lucru 
    FastAPI\app
        cu
            __init__.py     #de fata
            bazadedate1.py
            config.py       # introduce variabilele de mediu de lucru
            main14.py
            modele5.py      #introduce relatiile intre tabele
            util1.py
            validari6.py    #introduce validarile pentru jetoane

    FastAPI\app\rute
        cu
            __init__.py     #gol
            articole4.py    #introduce accesul la scriere in BD, numai cu drept atribuit utilizatorului
            autentif2.py
            oauth24.py    #introduce validarea jetoanelor  
            useri3.py

            
            
Implementeaza
    FastAPI Votes/like Theory file: Part #81 Python API Course de Sanjeev Thiyagarajan
    FastAPI Creating Votes Table pgadmin file: Part #82 Python API Course de Sanjeev Thiyagarajan
    FastAPI Votes SQLAlchemy file: Part #83 Python API Course de Sanjeev Thiyagarajan
    FastAPI Votes Route file: Part #84 Python API Course de Sanjeev Thiyagarajan

executat cu
    app>uvicorn main15:app --reload
    
structura de module (=fisiere) este

    FastAPI
        cu
            mediudelucru.env     #creat cu main 14 pentru variabilele de mediu de lucru
            .gitignore  #creat cu main 14 pentru variabilele de mediu de lucru 
    FastAPI\app
        cu
            __init__.py     #de fata
            bazadedate1.py
            config.py       # introduce variabilele de mediu de lucru
            main15.py
            modele6.py      #introduce relatiile intre tabele
            util1.py
            validari7.py    #introduce validarile pentru jetoane

    FastAPI\app\rute
        cu
            __init__.py     #gol
            articole6.py    #introduce accesul la scriere in BD, numai cu drept atribuit utilizatorului
            autentif3py
            oauth25.py    #introduce validarea jetoanelor  
            useri4.py
            voturi.py     #introduce votarea


Implementeaza
    FastAPI Votes/like Theory file: Part #81 Python API Course de Sanjeev Thiyagarajan
    FastAPI Creating Votes Table pgadmin file: Part #82 Python API Course de Sanjeev Thiyagarajan
    FastAPI Votes SQLAlchemy file: Part #83 Python API Course de Sanjeev Thiyagarajan
    FastAPI Votes Route file: Part #84 Python API Course de Sanjeev Thiyagarajan
    FastAPI SQL Joins/ SQLAlchemy file: Part #86 Python API Course de Sanjeev Thiyagarajan

executat cu
    app>uvicorn main16:app --reload
    
structura de module (=fisiere) este

    FastAPI
        cu
            mediudelucru.env     #creat cu main 14 pentru variabilele de mediu de lucru
            .gitignore  #creat cu main 14 pentru variabilele de mediu de lucru 
    FastAPI\app
        cu
            __init__.py     #de fata
            bazadedate1.py
            config.py       # introduce variabilele de mediu de lucru
            main16.py
            modele6.py      #introduce relatiile intre tabele
            util1.py
            validari8.py    #modificat fata de 7 pentru validarea articolelor cu vot

    FastAPI\app\rute
        cu
            __init__.py     #gol
            articole7.py    #modifcat fata de 6 pentru a adauga coloana voturi (JOIN)
            autentif4.py
            oauth26.py    #introduce validarea jetoanelor  
            useri5.py
            voturi1.py     #introduce votarea
        
            
Implementeaza
    FastAPI What is CORS: Part #?? Python API Course de Sanjeev Thiyagarajan
                                Alembic
                                Heroku

executat cu
    FastAPI>alembic upgrade head                #local actualizarea structurii BD
    FastAPI>uvicorn app.main17:app --reload     #local ansarea aplicatiei
    FastAPI>heroku "alembic upgrade head"       #pe Heroku  actualizarea structurii BD
    FastAPI>heroku "uvicorn app.main17:app"     #pe Heroku  lansarea aplicatiei

pentru pregatire
    git add --all                   #    actualizare GIThub copiere fisiere
    git commit -m "commit ultimul"    #    actualizare GIThub  fixare fisiere
    git push origin main    #    actualizare GIThub
    git push heroku main    #    actualizare si instalare app pe Heroku
    heroku ps:restart       #   pregatire app pe Heroku
    heroku logs             #   tiparire pe terminal

structura de module (=fisiere) este

    FastAPI
        cu
            .gitignore  #creat cu main 14 pentru ca de la incarcarea in GIT sa fie excluse 
                        #anumite fisiere si cataloage, de exemplu mediudelucru.env
            alembic.ini         # creat cu main16 pt pregatire actualizare BD cu Alembic
            Procfile    # creat cu main17 pentru Heroku
            mediudelucru.env    #creat cu main 14 pentru variabilele de mediu de lucru
            requirements.txt    # creat cu main17 pentru Heroku

    FastAPI\Alembic
        cu
            env.py
    FastAPI\Alembic\versions
        cu
            ????_creare_tabele.py
            ??????_crearea_relatii.py
    FastAPI\app
        cu
            __init__.py     #de fata
            oauth26.py    #introduce validarea jetoanelor  
            bazadedate1.py
            config.py       # introduce variabilele de mediu de lucru
            main17.py
            modele6.py      #introduce relatiile intre tabele
            requirements.txt #contine numele pachetelor python necesare dezvoltarii main17
            util1.py
            validari8.py    #modificat fata de 7 pentru validarea articolelor cu vot

    FastAPI\app\rute
        cu
            __init__.py     #gol
            articole7.py    #modifcat fata de 6 pentru a adauga coloana voturi (JOIN)
            autentif4.py
            useri5.py
            voturi1.py     #introduce votarea
        
            
            
'''