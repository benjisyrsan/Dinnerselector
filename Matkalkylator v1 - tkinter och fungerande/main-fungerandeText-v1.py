#-*- coding: utf-8 -*-


"""
Författare: Benjamin
Grundidè: Leona

"""

"""
allaRecept2 = [
    recept("gulash", [ingredient("potatis", 6, "st"), ingredient("morot", 3, "st")]),
    recept("soppa", [ingredient("potatis", 6, "st"), ingredient("morot", 3, "st")])
]
"""

import random

def recept2dict(filnamn: str):
    file = open(filnamn, encoding="utf-8")

    resultReceptlist = []
    curRecept = recept("", [])
    for line in file:
        if line == "\n": #add recept 2 dict
            resultReceptlist.append(curRecept)
            continue
        
        line = line.strip()
        if line[0] == "-": #titel
            curRecept = recept(line[1:], [])
            continue
          
        ingredientInfo = line.split()
        curIngredient = ingredient(ingredientInfo[0], 1, "st")
        if len(ingredientInfo) > 1:
            curIngredient.mängd = int(ingredientInfo[1])
            curIngredient.enhet = ingredientInfo[2]
        
        curRecept.ingredienser.append(curIngredient)

    file.close()
    return resultReceptlist

class ingredient:
    def __init__(self, namn = "", mängd = 0, enhet = "st"):
        self.namn = namn
        self.mängd = mängd
        self.enhet = enhet

    def __add__(self, other):
        return ingredient(self.namn, self.mängd + other.mängd, self.enhet) 
    
    def __eq__(self, other):
        return self.mängd == other.mängd

    def __lt__(self, other):
        return self.mängd < other.mängd

class recept:
    def __init__(self, namn, ingredienser):
        self.namn = namn
        self.ingredienser = ingredienser

def displayRecept(allaRecept: dict):
    for rec in allaRecept:
        rec: recept
        print("___" + rec.namn.upper() + "___")
        for ingr in rec.ingredienser:
            print("-", ingr.namn, ingr.mängd, ingr.enhet)
        print("")

def combineRecepts(allaRecept: list):
    resultat = []
    for rec in allaRecept:
        for ingr in rec.ingredienser: 
            #check if ingr exists
            didExist = False
            for i, ingrInResultat in enumerate(resultat):
                if ingr.namn == ingrInResultat.namn:
                    resultat[i] = ingrInResultat + ingr
                    didExist = True
            
            if not didExist:
                resultat.append(ingr)

    return resultat

def displayInköpslista(inköpslista: list):
    print("___INKÖPSLISTA___")
    for ingr in inköpslista:
        print("-", ingr.namn, ingr.mängd, ingr.enhet)
    print("")

def slumpaRecept(allaRecept: list, antal: int):
    result = []
    slumpadeIndex = []
    while len(slumpadeIndex) < antal:
        curRandom = random.randint(0, len(allaRecept)-1)
        if not curRandom in slumpadeIndex:
            slumpadeIndex.append(curRandom)

    for i in slumpadeIndex:
        result.append(allaRecept[i])

    return result

allaRecept = recept2dict("recept.txt")
slumpadeRecept = slumpaRecept(allaRecept, 4)
inköpsLista = combineRecepts(slumpadeRecept)
displayRecept(slumpadeRecept)
inköpsLista = sorted(inköpsLista, reverse=True)
displayInköpslista(inköpsLista)