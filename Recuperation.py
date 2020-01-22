import json
import os
values=[]
table=dict()
nomTable=""
def GeAttributAndType(nomDB,TableName):
    tab=dict()
    with open(nomDB, 'r') as fp:
        dic = json.load(fp)
    
    for cle in dic[TableName]:
            for key in cle:
            #tab.append(key)
                tab[key]=dic[TableName][0][key]
            break 
    return tab
def typeParDefaut(nomFichier,TableName):
    with open(nomFichier, 'r') as fp:
        dic = json.load(fp)
    
    for cle in dic[TableName]:
            for key in cle:
            #tab.append(key)
                if dic[TableName][0][key][0]=="":
                    dic[TableName][0][key][0]="varchar(50)"
                if dic[TableName][0][key][1]=="":
                    dic[TableName][0][key][1]="null"

            break 
    with open(nomFichier, "w") as write_file:
        write_file.write(json.dumps(dic, indent=4))
    print("Creation de la table %s reussit :)" % TableName)
def listeContraintes():
    return ["null",'PRIMARY KEY','UNIQUE','REFERENCES','CHECK ','FOREIGN KEY']
def listeType():
    return ['number','smalling','integer','float','date','time','timestamp','char','varchar']
def ControlType(nomDB,TableName,attribut):
    for typ in listeType():
        if getType(nomDB,TableName,attribut).startswith(typ):
            print(typ)
            return 1
        else:
            pass
    print("Ce type %s  n'est pas définis" % getType(nomDB,TableName,attribut) )
    return 0
def ControlContrainte(nomDB,TableName,attribut):
    for contrainte in listeContraintes():
        if getContraintes(nomDB,TableName,attribut).casefold().startswith(contrainte.casefold()):
           return 1
        else:
            pass
    print("Cette contrainte %s n'est pas définis" % getContraintes(nomDB,TableName,attribut) )
    return 0
def ControlTypeAndContrainte(nomDB,TableName):
    tab=GetAtributName(nomDB,TableName)
    for attribut in tab:
        print(attribut)
        if (ControlContrainte(nomDB,TableName,attribut)==0 or ControlType(nomDB,TableName,attribut)==0):
            return 0
    return 1
def getType(nomDB,TableName,attribut):
    tab=GeAttributAndType(nomDB,TableName)
    return tab[attribut][0]
def getContraintes(nomDB,TableName,attribut):
    tab=GeAttributAndType(nomDB,TableName)
    return tab[attribut][1]

def DropDB(user,nomDB):
    if isAbility(user,nomDB,'d') and nomDB!="":
        try:
            os.remove(nomDB)
            deletenNameDB(nomDB)
            print("Suppression de la base de données reussit :)")
        except Exception as error:  
            print("base de données introuvable")
    else:
        return "Vous n'etes pas abilité à supprimer la base de données"
def renameDB(user,nomDB,newName):
    if isAbility(user,nomDB,'w') and nomDB!="":
        try:
            os.rename(nomDB,newName)
            modifynNameDB(nomDB,newName)
            return True
        except Exception as error:  
            return "base de données introuvable"
    else:
        return "Vous n'etes pas abilité à modifier le nom de la base de données"
def CreateDB(user,nomDB):
    if nomDB!="":
        with open(nomDB, 'w') as fp:
            pass
        modifyAcces("admin","admin",user,nomDB,"rwd")
        modifyAcces("admin",user,nomDB,"rwd")
        return "Creation de la base de données %s reussit :)" % nomDB
    else:
        return "Veuilez vous connecter d'abord"

def CreateTable(user,nomFichier,TableName,AttributList):
    if isAbility(user,nomFichier,'w'):    
        tmp=0
        try:
            with open(nomFichier, 'r') as fp:
                dic = json.load(fp)
        except Exception as error:    
            dic=dict()
        for objet in dic:
            if objet==TableName:
                tmp=1
        if tmp==0:
            Tableau=[]
            Tableau.append(AttributList)
            dic[TableName]=Tableau
            #print ("%s" %(Tableau))
            with open(nomFichier, "w") as write_file:
                write_file.write(json.dumps(dic, indent=4))
            typeParDefaut(nomFichier,TableName)
            return "Creation de la table %s reussit :)" % TableName

            if ControlTypeAndContrainte(nomFichier,TableName)==0:
                DropTable(user,nomFichier,TableName)
    else:
        return "Vous n'étes pas abilté à modifier les information de la base de données"       
        
def FirstCreateTable(nomFichier,TableName,AttributList):
    dic=dict()
    Tableau=[]
    Tableau.append(AttributList)
    dic[TableName]=Tableau
    print ("%s" %(Tableau))
    with open(nomFichier, "w") as write_file:
        write_file.write(json.dumps(dic, indent=4))
    typeParDefaut(nomFichier,TableName)       
    return "Création reussit :)"
def GetAtributName(nomFichier,TableName):
    tab=[]
    with open(nomFichier, 'r') as fp:
        dic = json.load(fp)
    for cle in dic[TableName]:
            for key in cle:
                tab.append(key)
            break 
    return tab
def showDataBase(user,NameDB):
    if isAbility(user,NameDB,'r'):    
        try:
            with open(NameDB, 'r') as fp:
                dic = json.load(fp)
                tmp=[]
                for tab in dic:
                    tmp.append(tab)
                return tmp
        except Exception as error:
            return "la base de données n'existe pas"
    else:
        return "Vous n'étes pas abilté à voir les informations de la base de données"
    

def AddValues(user,nomFichier,TableName,AttributList):
    if isAbility(user,nomFichier,'w'):    
        tmp=0
        
        with open(nomFichier, 'r') as fp:
            dic = json.load(fp)
        for objet in dic:
            if objet==TableName:
                tmp=1
        tab=[]
        if tmp==1:
            for cle in dic[TableName]:
                for key in cle:
                    tab.append(key)
                break
            dictionnaire=dict()
            i=0
            for i in range(len(tab)):
                dictionnaire[tab[i]]=AttributList[i]
                
            dic[TableName].append(dictionnaire)
            
            #print ("%s" %(Tableau))
            with open(nomFichier, "w") as write_file:
                write_file.write(json.dumps(dic, indent=4))
            return "Ajout reussit :)" 
    return "Vous n'étes pas abilté à modifier les information de la base de données"   
#Cette fonction prends en parametre le nom de ba base,Table,nomde l'attribut et [type,contrainte]        
def AlterAlterAttribut(user,DataBase,TableName,AttributName,AttributValue):

    if isAbility(user,DataBase,'w'):     
        with open(DataBase, 'r') as fp:
                dic = json.load(fp)
        #dic[TableName][AttributName]=AttributValue
        for attr in dic[TableName]:
            attr[AttributName]=AttributValue
            break
        with open(DataBase, 'w') as write_file:
            write_file.write(json.dumps(dic, indent=4))
        return "Modification reussit :)"
    else:
        return "Vous n'étes pas abilté à modifier les information de la base de données"
def AlterEnregistrement(user,DataBase,TableName,attributName,value,newValue):
    if isAbility(user,DataBase,'w'): 
        with open(DataBase, 'r') as fp:
                dic = json.load(fp)
        i=0
        #dic[TableName][AttributName]=AttributValue
        for attr in dic[TableName]:
            if i==0:
                i+=1
            else:
                if attr[attributName]==value:
                    attr[attributName]=newValue
            
        with open(DataBase, 'w') as write_file:
            write_file.write(json.dumps(dic, indent=4))
        return "Modification reussit :)"
    else:
        return "Vous n'étes pas abilté à modifier les information de la base de données"
def DropTable(user,DataBase,TableName):
    if isAbility(user,DataBase,'d'):   
        with open(DataBase, 'r') as fp:
                dic = json.load(fp)
        del dic[TableName]
        with open(DataBase, 'w') as write_file:
            write_file.write(json.dumps(dic, indent=4))
        return "Suppression reussit :)"
    else:
        return "Vous n'étes pas abilté à modifier les information de la base de données"
def DropValues(user,DataBase,TableName,attributName,value):
    if isAbility(user,DataBase,'d'):
        with open(DataBase, 'r') as fp:
            dic = json.load(fp)
            newTable=dic[TableName]
            copy=[]
            del dic[TableName]
        for values in newTable:
            if values[attributName]!=value:
                copy.append(values)
        del newTable
        dic[TableName]=copy
        
        #del dic[TableName]
        with open(DataBase, 'w') as write_file:
            write_file.write(json.dumps(dic, indent=4))
        return "Suppression reussit :)"
    else:
        return "Vous n'étes pas abilté à supprimer les information de la base de données"
def renameTable(user,DataBase,TableName,NewName):
    if isAbility(user,DataBase,'w'):
        with open(DataBase, 'r') as fp:
                dic = json.load(fp)
        test=dic[TableName]
        del dic[TableName]
        dic[NewName]=test
        with open(DataBase, 'w') as write_file:
            write_file.write(json.dumps(dic, indent=4))
        return True
    else:
        return "Vous n'étes pas abilté à modifier les information de la base de données"
def DropAttribut(user,DataBase,TableName,AttributName):
    if isAbility(user,nomFichier,'d'):
        with open(DataBase, 'r') as fp:
                dic = json.load(fp)
        for dics in dic[TableName]: 
            del dics[AttributName]
        with open(DataBase, 'w') as write_file:
            write_file.write(json.dumps(dic, indent=4))
        return "Suppression reussit :)"

    else:
        return "Vous n'étes pas abilté à supprimer les information de la base de données"
def AddAttribut(user,DataBase,TableName,AttributName,AttributValue):
    if isAbility(user,DataBase,'w'):
        test={}
        try:
            with open(DataBase, 'r') as fp:
                dic = json.load(fp)
            i=0
            for dics in dic[TableName]:
                if i==0:
                    test=dics
                    del dics
                    test[AttributName]=AttributValue
                    dics=test
                    print(test)
                    i+=1
                else:
                    test=dics
                    del dics
                    test[AttributName]=""
                    dics=test
                    print(test)

            try:
                with open(DataBase, 'w') as write_file:
                    write_file.write(json.dumps(dic, indent=4))
                return "Ajout reussit :)"
                            
            except Exception as error:
                return "invalid json: %s" % error
                ok = False
                
        except Exception as error:
            print("la base de données ou table introuvable ")
            ok = False
    else:
        return "Vous n'étes pas abilté à modifier les information de la base de données"
def selectTout(user,database,table):
    if isAbility(user,database,'r'):
        dice= []
        try:
            with open(database, 'r') as fp:
                dic = json.load(fp)  
            i=0
            for value in dic[table]:
                if i==0: 
                    i+=1
                    continue
                dice.append(value)   
            return dice 
        except Exception as error:
            print( "fichier utilisateur introuvable")
    else:
        return "Vous n'étes pas abilté à lire les information de la base de données"
def selectToutWhere(user,database,table,attribut,value):
    dic=selectTout(user,database,table)
    tmp=[]
    try:  
        for valu in dic:
            if valu[attribut]==value:
                tmp.append(valu)
        return tmp
    except Exception as error:
            print("invalid json: %s" % error)
  
def selectAttributWhere(user,database,table,attibuts,attribut,value):
    dic=selectToutWhere(user,database,table,attribut,value)
    tmp=[]
    try:   
        for champs in dic:
            chaine=dict()
            for att in attributs:
                chaine[att]=champs[att]
            tmp.append(chaine)
        return tmp
    except Exception as error:
            print("invalid json: %s" % error)
def DropUser(user,TableName):
    if user=="admin":   
        with open("Users.json", 'r') as fp:
                dic = json.load(fp)
        del dic[TableName]
        with open("Users.json", 'w') as write_file:
            write_file.write(json.dumps(dic, indent=4))
        return "Suppression reussit :)"
    else:
        return "Vous n'étes pas abilté à modifier les information de la base de données"

def selectAttribut(user,database,table,attribut):
    dic=selectTout(user,database,table)
    tmp=[]
    for champs in dic:
        chaine=dict()
        for att in attribut:
            chaine[att]=champs[att]
        tmp.append(chaine)

    return tmp       
def createUser(user,login,password,listeDB):
    if user=='admin':
        try:
            with open('users.json', 'r') as fp:
                dic = json.load(fp)       
        except Exception as error:
            return "fichier utilisateur introuvable"
            dic=dict()
        tmp=dict()
        tmp['login']=login
        tmp['password']=password
        tmp['listeDB']=listeDB
        dic[login]=tmp
        with open('users.json', 'w') as write_file:
                write_file.write(json.dumps(dic, indent=4))
        return  "Creation de l'utlisateur %s reussit" % login
    else:
        return "Désolé seul l'administrateur peut creer un utilisateur"
def isHere(login,password):
    try:
        with open('users.json', 'r') as fp:
            dic = json.load(fp) 
        if dic[login]["login"]==login and dic[login]["password"]==password :
            return True
        else:
            print("Utilisateur non trouvé :)")
    except Exception as error:
        return "fichier utilisateur introuvable"
def isAbility(login,database,mode):
    try:
        with open('users.json', 'r') as fp:
            dic = json.load(fp)
    except Exception as error:
        return "fichier utilisateur introuvable"
    try:
            #print(dic[login]["listeDB"][db])
            if mode in dic[login]["listeDB"][database]:
                return True
            else:
                return "login n'a pas le mode d'acces %s"% mode
    except Exception as error:
        return "vous  n'est pas autorisé à manipuler la base de données %s "% database    

        print("Utilisateur non trouvé :)")
    except Exception as error:
        return "fichier utilisateur introuvable"
def showUser(user,login):
    if user=="admin":   
        try:
            with open('users.json', 'r') as fp:
                dic = json.load(fp)
        except Exception as error:
            return "fichier utilisateur introuvable"
        return dic[login]['listeDB']
    else:
        return "Désolé seul l'administrateur a le droit de voir la liste des utilisateurs"
def showUsers(login):
    try:
        with open('users.json', 'r') as fp:
            dic = json.load(fp)
    except Exception as error:
        return "fichier utilisateur introuvable"
    dicti=dict()
    for user in dic:
        dicti[user]=showUser(login,user)
    return dicti
def modifyAcces(user,login,database,mode):
    if user=="admin":

        try:
            with open('users.json', 'r') as fp:
                dic = json.load(fp)
            db=dict(dic[login]['listeDB'])
            del dic[login]['listeDB']
            db[database]=mode
            dic[login]['listeDB']=db
            with open('users.json', 'w') as write_file:
                write_file.write(json.dumps(dic, indent=4))  
            return "modification reussit :)"
        except Exception as error:
            return "fichier utilisateur introuvable"
    else:
        return "Seul l'administrateur du serveur de base de données est abilité à faire des gestions de privileges"
def deleteAcces(user,login,database):
    if user=="admin":
        try:
            with open('users.json', 'r') as fp:
                dic = json.load(fp)
        except Exception as error:
            return "fichier utilisateur introuvable"
        try:
            del dic[login]['listeDB'][database]
            with open('users.json', 'w') as write_file:
                write_file.write(json.dumps(dic, indent=4))  
            return "modification reussit :)"
        except Exception as error:
            return "Utilisateur ou base de données introuvable " 
    else:
        return "Seul l'administrateur du serveur de base de données est abilité à faire des gestions de privileges"
def modifyUser(login,newLogin,newPassword):
    try:
        with open('users.json', 'r') as fp:
            dic = json.load(fp)
        #return "Modification de l'utilisateur %s reussit :)" %newLogin
    except Exception as error:
        return "fichier utilisateur introuvable"
    
    try:
        tmp= dic[login]
        del  dic[login]
        tmp['login']=newLogin
        tmp['password']=newPassword
        dic[newLogin]=tmp
        with open('users.json', 'w') as write_file:
            write_file.write(json.dumps(dic, indent=4))
        return "Modification reussit :) "
    except Exception as error:
        return "Utilisateur introuvable ou login et mot de passe introuvable "
   
def saisie2(nomTable,values):
    print("Bienvenue sur creation table")
    print("Veuiller entrer le nom de table")
    nomTable=input()
    attri=GetAtributName("Teste.json",nomTable)
    for i in range(0,4):
        print("Veuillez entrer le type de l'attribut %s" % attri[i])
        values.append(input())
    AddValues("Teste.json",nomTable,values)
    for value in values:
        print(value)
def saisi1():
    nom=""
    typ=""
    contrainte=""
    
    print("Bienvenue sur creation table")
    print("Veuiller entrer le nom de table")
    nomTable=input()
    for i in range(0,4):
        tab=[]
        print("Veuillez entrer le nom de l'attribut ")
        nom=input()
        print("Veuillez entrer le type de l'attribut ")
        typ=input()
        print("Veuillez entrer la contrainte de l'attribut ")
        contrainte=input()
        tab.append(typ)
        tab.append(contrainte)
        table[nom]=tab
    #AddValues("Etudiant.json",nomTable,values)
    CreateTable("Teste2.json",nomTable,table) 
def deletenNameDB(name):
    try:
        with open('users.json', 'r') as fp:
            dic = json.load(fp)
    except Exception as error:
        return "fichier utilisateur introuvable"
    i=0
    tab=dict()
    for user in dic:
        #print(dic[user]['listeDB'])
        tmp=dict(dic[user]['listeDB'])
        del dic[user]['listeDB']
        for db, mode in tmp.items():
            if db==name:
               pass
            else:
               tab[db]=mode
        dic[user]['listeDB']=tab 
        
    try:
        with open('users.json', 'w') as write_file:
            write_file.write(json.dumps(dic, indent=4))  
    except Exception as error:
        return "Utilisateur ou base de données introuvable " 
def modifynNameDB(name,newname):
    try:
        with open('users.json', 'r') as fp:
            dic = json.load(fp)
    except Exception as error:
        return "fichier utilisateur introuvable"
    i=0
    
    for user in dic:
        #print(dic[user]['listeDB'])
        tab=dict()
        tmp=dict(dic[user]['listeDB'])
        del dic[user]['listeDB']
        for db, mode in tmp.items():
            if db==name:
                tab[newname]=mode
            else:
               tab[db]=mode
        dic[user]['listeDB']=tab 
        
    try:
        with open('users.json', 'w') as write_file:
            write_file.write(json.dumps(dic, indent=4))  
    except Exception as error:
        return "Utilisateur ou base de données introuvable " 
if __name__ == '__main__':
    pass
    modifynNameDB("bonjour .json","bonjour1.json")
    #deletenNameDB("bonjour1.json")
    #print(createUser("khadyba","aliou",{"Teste.json":"rwd","bonjour .json":"r"}))
    #print(isHere("abdouseck632","bonjour"))
    #print(isAbility("khadyba","Teste.json","e"))
    #print(modifyAcces("abdouseck","bonjour .json","rwd"))
    #print(deleteAcces("abdouseck","bonjour .json"))
    #print(selectAttributWhere("abdouseck","Teste.json","Awa",["id","nom"],"id","441992"))
    #print(selectAttribut("abdouseck","Teste.json","Awa",["id","nom"]))
    #selectTout("abdouseck","Teste.json","Awa")
    #print(modifyUser("abdouseck632","abdouseck","seck96"))
    #saisi1()
    #print (showDataBase("Teste.json"))
    #DropDB("montest.json")
    #CreateDB("abdouseck","Parc2.json")
    renameDB("abdouseck","Base.json","Base1.json")
    #saisie2(nomTable,values)
    #saisi1()
    #DropValues('Etudiant.json','Classe','id',"201")
    #table[nom]=type
    #print(GetAtributName("Etudiant.json","Classe"))
    #FirstCreateTable("Etudiant.json",nomTable,table)
    """CreateTable("abdouseck","Parc2.json","animal",
        {
            "id": [
                "integer",
                "primary key"
            ],
            "prenom": [
                "varchar(50)",
                "check"
            ],
            "nom": [
                "varchar(100)",
                ""
            ],

            "age": [
                "integer",
                "check"
            ]
        }
    )"""
    #AddValues("Etudiant.json",nomTable,values)
    #DropTable('Teste.json','Awa')
    #getContraintes('Teste.json','Awa','id')
    #typeParDefaut('Teste.json','Personne')
    #print(ControlType('Teste.json','Personne','nom'))
    #print(ControlTypeAndContrainte('Teste.json','Personne'))
    #print(ControlTypeAndContrainte('Teste.json','Personne'))
    #AddAttribut('Teste.json','Awa',"adresse",['varchar(100)', 'not null']) 
    #AlterAttribut('Teste.json',"Awa","nom",["varchar(20)","not null"]) 
    #AlterEnregistrement("Teste.json","Awa","id","201","441992")
    #DropAttribut('bonjour .json','table',"age") 
    #CreateDB("Etudiant.json")
    
    
    
    