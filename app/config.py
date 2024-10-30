'''
Fisier:
    FastAPI/app/config.py

Autor:
    Adrian Popescu

Proiect
    management de documente cu Python prin FastAPI
    Implementeaza FastAPI Environment Variables: Part #80 Python API Course dr Sanjeev Thiyagarajan

Scop:
    stabilirea variabilelor "de mediu" necesare in dezvoltarea si apoi exploatarea aplicatiei

Versiune anterioara:
    Nu exista
'''

from pydantic_settings import BaseSettings   #importa clasele de validare a variabilelor "de mediu"

'''
class MediuLucru(BaseSettings):   #clasa variabilelor de mediu; folosesc denumirile conventionale in EN
                                #buna practica este ca numele sa fie cu majuscule, dar, vezi mai jos
    DB_hostname: str = "localhost" #stabilire valoare implicita pt cazul in care nu-i def in fis env
    DB_port: str = "5432" #stabilire valoare implicita pt cazul in care nu-i def in fis env
    DB_password: str = "Superadmin" #stabilire valoare implicita pt cazul in care nu-i def in fis env
    DB_name: str = "fastapi" #stabilire valoare implicita pt cazul in care nu-i def in fis env
    DB_username: str = "postgres" #stabilire valoare implicita pt cazul in care nu-i def in fis env
#    DB_username: str = "postgres" #stabilire valoare implicita pt cazul in care nu-i def in fis env
    algoritmcriptare: str = "HS256" #stabilire valoare implicita pt cazul in care nu-i def in fis env
    cheiesecreta: str = "abcdef0816242539abcdef34269723765abcdef90814376543abcdef876236bd"  #stabilire valoare implicita pt cazul in care nu-i def in fis env
    duratavalabilitatejeton: int = # UM = min

    class Config:
        env_file = "..\mediudelucru.env"   #numele fisierului care contine variabilele de configurare
                                            #  in productie se va numi altfel
'''
class MediuLucru(BaseSettings):   #clasa variabilelor de mediu; folosesc denumirile conventionale in EN
                                #buna practica este ca numele sa fie cu majuscule, dar, vezi mai jos
    
    DB_hostname: str
    DB_port: str
    DB_password: str 
    DB_name: str
    DB_username: str
    algoritmcriptare: str
    cheiesecreta: str
    duratavalabilitatejeton: int

    class Config:
        env_file = ".env"   #numele fisierului care contine variabilele de configurare
                                            #  in productie se va numi altfel
    
mediu = MediuLucru()    #obiectul care contine valorile variabilelor de mediu (constantele mediului de lucru)
                        #pydantic va transforma in litere mari toate denumirile variabilelor de mediu
                        #   si va verifica tipul str pentru toate

print("[config.py] mediu.DB_username = ", mediu.DB_username, ", mediu.duratavalabilitatejeton = ", mediu.duratavalabilitatejeton )  #pt test
