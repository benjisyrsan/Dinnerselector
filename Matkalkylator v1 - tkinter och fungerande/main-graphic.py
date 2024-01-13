#-*- coding: utf-8 -*-

"""
Författare: Benjamin
Grundidè: Leona

allaRecept = [
    recept("gulash", [ingredient("potatis", 6, "st"), ingredient("morot", 3, "st")]),
    recept("soppa", [ingredient("potatis", 6, "st"), ingredient("morot", 3, "st")])
]
"""

import random
import tkinter as tk

def recept2list(filnamn: str):
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
        
        try:
            curIngredient.position = ingredienterDict[curIngredient.namn]["position"]["value"]
        except:
            curIngredient.position = 0

        curRecept.ingredienser.append(curIngredient)

    file.close()
    return resultReceptlist

def ingredienter2dict(filnamn: str):
    #{'potatis': {'position': {'value': 5, 'enhet': ''}, 
    # 'pris': {'value': 20, 'enhet': 'kr'}, 
    # 'energi': {'value': 200, 'enhet': 'kcal'}}
    file = open(filnamn, encoding="utf-8")

    resultDict = {}
    curIngredient = {}
    curNamn = ""
    for line in file:
        if line == "\n": #add recept 2 dict
            resultDict[curNamn] = curIngredient
            curIngredient = {}
            continue
        
        line = line.strip()
        if line[0] == "-": #titel
            curNamn = line[1:]
            continue
          
        ingredientInfo = line.split()
        if len(ingredientInfo) < 3:
            ingredientInfo.append("")

        curIngredient[ingredientInfo[0]] = {"value": int(ingredientInfo[1]), "enhet": ingredientInfo[2]}

    file.close()
    return resultDict

class ingredient:
    def __init__(self, namn = "", mängd = 0, enhet = "st", position = 10):
        self.namn = namn
        self.mängd = mängd
        self.enhet = enhet
        self.position = position

    def __add__(self, other):
        return ingredient(self.namn, self.mängd + other.mängd, self.enhet, self.position) 
    
    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.position < other.position

class recept:
    def __init__(self, namn, ingredienser):
        self.namn = namn
        self.ingredienser = ingredienser

def displayRecept(allaRecept):
    for i, rec in enumerate(allaRecept):
        rec: recept
        print("___" + rec.namn.upper() + " nr: " + str(i) + "___")
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

    #slumpadeIndex = [8, 11, 12, 14]
    for i in slumpadeIndex:
        result.append(allaRecept[i])

    return result

def add2IngridienterTXT(lista: list):
    file = open("ingredienter.txt", "a", encoding="utf-8")
    for ingr in lista:
        ingr: ingredient
        if not ingredienterDict.get(ingr.namn):
            file.write("-" + ingr.namn + "\n" + "position 0\npris 0 kr\nenergi 0 kcal\n\n")
            print("ny ingrediens: " + ingr.namn)
    
    file.close()


ingredienterDict = ingredienter2dict("ingredienter.txt")
allaRecept = recept2list("recept.txt")
add2IngridienterTXT(combineRecepts(allaRecept))
slumpadeRecept = slumpaRecept(allaRecept, 4)
inköpsLista = combineRecepts(slumpadeRecept)
inköpsLista = sorted(inköpsLista, reverse=False)

#displayRecept(allaRecept)
#displayInköpslista(inköpsLista)



#display graphic
def slumpButtonClick():
    slumpadeRecept = slumpaRecept(allaRecept, 4)
    inköpsLista = combineRecepts(slumpadeRecept)
    inköpsLista = sorted(inköpsLista, reverse=False)

    for i, rec in enumerate(slumpadeRecept):
        rec: recept
        dispText = rec.namn.upper() + "\n"
        for ingr in rec.ingredienser:
            dispText += "- " + ingr.namn + " " + str(ingr.mängd) + " " + ingr.enhet + "\n"
        recText = recTexts[i]
        recText["text"] = dispText

    dispText = "INKÖPSLISTA \n"
    for ingr in inköpsLista:
        dispText += "- " + ingr.namn + " " + str(ingr.mängd) + " " + ingr.enhet + "\n"

    inköpText["text"] = dispText


root = tk.Tk()
root.title("Matväljaren")
root.geometry("900x500")
root["bg"] = "azure"

recTexts = []

for rec in slumpadeRecept:
    rec: recept
    dispText = rec.namn.upper() + "\n"
    for ingr in rec.ingredienser:
        dispText += "- " + ingr.namn + " " + str(ingr.mängd) + " " + ingr.enhet + "\n"

    recText = tk.Label(root, text=dispText, bg="gold", justify="left", anchor="n", height=15, pady=10)
    recText.pack(side=tk.LEFT, ipadx=20, ipady=20, padx=5, pady=5)
    recTexts.append(recText)

dispText = "INKÖPSLISTA \n"
for ingr in inköpsLista:
    dispText += "- " + ingr.namn + " " + str(ingr.mängd) + " " + ingr.enhet + "\n"

inköpText = tk.Label(root, text=dispText, bg="turquoise", justify="left", anchor="n", pady=10)
inköpText.pack(side=tk.RIGHT, ipadx=20, ipady=20, padx=5, pady=5)
slumpaNyaButton = tk.Button(text="Slumpa", command=slumpButtonClick)
slumpaNyaButton.pack()

root.mainloop()