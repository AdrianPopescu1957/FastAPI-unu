'''
Fisier
    FastAPI/app/util1.py

Autor
    Adrian Popescu

Proiect
    management de documente cu Python prin FastAPI
Implementeaza
    FastAPI Environment Variables.py file: Part #80 Python API Course de Sanjeev Thiyagarajan

Scop
    functii utile

Versiune anterioara
    Fast/app/util.py

'''

#
#   functii si metode utile
#   asociata cu main10.py si, eventual, succesoarele sale
#


from passlib.context import CryptContext    #pentru criptarea parolei

# criptare cu Bcrypt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  
    #stabileste ca altgoritmul de criptare este Bcrypt

def hash(date: str):  # cripteaza un sir de caractere cu functia hash
    return pwd_context.hash(date)

# verificare valori hash
# compara valoarea functiei hash a parolei comunicate cu sirul cunoscut in BD
# problema rezolvata in util.py, desi codul e scurt, deoarece aici sint deja 
#   importate bibliotecile criptografice
'''
#cod slab
def compara(parolaprimita, parolastocata):
    if pwd_context.verify(parolaprimita, parolastocata):
        return True
    else:
        return False
        '''

def compara(parolaprimita, parolastocata):
    return pwd_context.verify(parolaprimita, parolastocata)
