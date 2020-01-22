import json
import sys
point=".json"

argv ="%s %s" % (sys.argv[1],".json")
def AjoutAttribut(Attribut,TableName):
    with open(nomFichier, 'r') as fp:
                dic = json.load(fp)

def CreateTable(nomFichier,TableName,AttributList):
    #Ajouter un table
    
    with open(nomFichier, 'r') as fp:
        dic = json.load(fp)
    dic[TableName]=AttributList
    print ("%s" %(table))
    with open(nomFichier, "w") as write_file:
        write_file.write(json.dumps(dic, indent=4))
                
    
    
if __name__ == '__main__':
    nom=""
    typ=""
    table=dict()
    print("Bienvenue veillez entrer le nom de la table ")
    nomTable=input()
    for i in range(4):
        print("Bienvenue veillez entrer le nom de l'attribut")
        nom=input()
        print("Bienvenue veillez entrer le type de l'attribut")
        typ=input()
        table[nom]=typ
    CreateTable("bonjour .json",nomTable,table)
