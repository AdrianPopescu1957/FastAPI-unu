#creaza modelul de date pentru baza de date Base definita in modulul bazadedate.py
# in cazul de fata model = tabela
#
# legatura intre baza de date si modelul datelor continute se face in main.py!
#
from sqlalchemy import Column, Integer 
from ..app.bazadedate import Baza

class Post(Baza):   #creaza clasa obiectelor afisate, obiecte care sint inregistrari ale bazei relationale Baza!
    __tablename__ = "afisari"   #creaza tabela afisari (articole = afise... = postari)

    id = Column(Integer, primary_key=True, nullable=False)  #creata fiecare coloana cu caracteristicile ei
    titlu = Column(str, nullable=False )    #titlul articolului (afisului)
    continut = Column(str, nullable=False )
    afisat = Column (bool, default=True)    #se presupune implicita dorinta ca articolul sa fie afisat la creare
# data si ora creerii mai tirziu!