from ..models import Statistika, NarudzbaBroj, Jelo
from .. import db


def calcStats():
    brojNarudzbi = 0
    promet = 0.0
    for narudzba in NarudzbaBroj.query.all():
        brojNarudzbi+=1
        promet+=narudzba.narudzbaCijenaDostave 

    brojNarudzbi = len(NarudzbaBroj.query.all()) #ocito count ne radi kak spada

    stats = Statistika.query.all()
   
    for stat in stats:
        promet += stat.cijena #lol a da ipak stavimo cijenu

    prosjecnaCijenaNarudzbe = 0.0

    if brojNarudzbi != 0:
        prosjecnaCijenaNarudzbe = promet / brojNarudzbi

    sql = "SELECT jeloID, COUNT (statistikaID) AS stats FROM Statistika GROUP BY jeloID ORDER BY stats DESC" #ovo za zadnji mjesec hahah
    najNarucivanije = db.engine.execute(sql)

    top3 = []
    i = 0
    
    for el in najNarucivanije:
        top3.append(el)
        i+=1
        if i == 3:
            break


    print ("promet {}, prosječnaCijenaNarudžbe {}".format(promet, prosjecnaCijenaNarudzbe))
    
    finTop3 = []

    for el in top3:
        jelo = Jelo.query.filter_by(jeloID=int(el[0])).first().naziv
        print( "Naziv {}, količina {}".format(jelo, el[1]) )
        finTop3.append( (jelo, el[1]) )

    return (promet, prosjecnaCijenaNarudzbe, finTop3)
