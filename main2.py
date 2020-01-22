from flask import Flask, request
from flask_restplus import Api, Resource
from Recuperation import *
NameDB=""
login=""
password=""
app = Flask(__name__)
api = Api(app=app)
db_Connexion = api.namespace('Connexion', description = "Connexion ou déconnexion pour utilisateur")
db_SelectionDB = api.namespace('selectionDB', description = "Sélection d'une base de données")
db_select = api.namespace('Select', description = "Affichage des informations de la table sélectionnné")
db_modifierUtilisateur = api.namespace('UpdateUser', description = "Modification des identifiants et mot de passe d'un utilisateur")
db_Attribut = api.namespace('attribut', description = "Manipulation des attributs avec la possibilité de insertion update delete attribut")
ns_Enregistrement = api.namespace('enregistrement', description = "Permet l'insertion la modification et la suppression d'enregistrement")
db_RenameDB = api.namespace('Base_de_données', description = "Connexion et décnnexion")
db_Utilisateur = api.namespace('Utilisateur', description = "Suppression-modificatio-suppresion des utilisateurs")
ns_Table = api.namespace('table', description = "Table operations")
ns_Privilege = api.namespace('privilege', description = "Permet de donner un privilege a un utilisateur de manipulation des bases de données")

def IsIdentified():
    if NameDB=="":
        return "vous n'etes pas encore choisit de base de données"
    return True
@db_Utilisateur.route("/<string:Utilisateur>/<string:mdp>")
class Utilisateurs(Resource):
    def post(self,Utilisateur,mdp):
        """
        Ajouter un nouveau utilisateur
        """
        return createUser(login,Utilisateur,mdp,"")
@ns_Privilege.route("/<string:identifiantUtilisateur>/<string:nomDB>/<string:modeAccess>")
class Attribut(Resource):
     
        
    def post(self,identifiantUtilisateur,modeAccess,nomDB):
        """
        Ajouter un attribut dans une tablle
        """
        tmp=""+nomDB+".json"
        return modifyAcces(login,identifiantUtilisateur,tmp,modeAccess)
    
    def put(self,identifiantUtilisateur,modeAccess,nomDB):
        tmp=""+nomDB+".json"
        return modifyAcces(login,identifiantUtilisateur,tmp,modeAccess)

@ns_Privilege.route("/<string:identifiantUtilisateur>/<string:nomDB>")
class Attribut(Resource):

    def delete(self,identifiantUtilisateur,nomDB):
        tmp=""+nomDB+".json"
        return deleteAcces(login,identifiantUtilisateur,tmp)
@db_modifierUtilisateur.route("<string:nouveau_Identifiant>/<string:nouveau_Mot_de_passe>")
class UpdateUtilisateur(Resource):
    def get(self,nouveau_Identifiant,nouveau_Mot_de_passe):
        """
        Modifier l'identifiant et le mot de passe d'un utilisateur
        """
        return modifyUser(login,nouveau_Identifiant,nouveau_Mot_de_passe)
@db_Utilisateur.route("/")
class showusers(Resource):
    def get(self):
        """
        Afficher a liste des bases d'un utilisateur
        """
        return showUsers(login)
@db_Utilisateur.route("/<string:Utilisateur>")
class userdelGet(Resource):
    def get(self,Utilisateur):
        """
        Afficher a liste des bases d'un utilisateur
        """
        return showUser(login,Utilisateur)
    def delete(self,Utilisateur):
        """
        Supprimer un utilisateur
        """
        return DropUser(login,Utilisateur)
@ns_Enregistrement.route("/<string:nomTable>")
class Attribut(Resource):
    def get(self,nomTable):
        """
        Faire un select par rapport a un attribut
        """
        #li=[nomAttribut]
        return selectTout(login,NameDB,nomTable)
    def post(self,nomTable):
        """
        Ajouter un attribut dans une tablle
        """
        data=request.get_json()
        return AddValues(login,NameDB,nomTable,data)

@ns_Enregistrement.route("/<string:nomTable>/<string:nomAttribut>/<string:valeurAttribut>")
class Attribut(Resource):
    def delete(self,nomTable,nomAttribut,valeurAttribut):
         
        return DropValues(login,NameDB,nomTable,nomAttribut,valeurAttribut)
@ns_Enregistrement.route("/<string:nomTable>/<string:nomAttribut>/<string:valeurAttribut>/<string:nouvelleValeur>")
class Attribut(Resource):
    def put(self,nomTable,nomAttribut,valeurAttribut,nouvelleValeur):
         
        return AlterEnregistrement(login,NameDB,nomTable,nomAttribut,valeurAttribut,nouvelleValeur)
@db_Attribut.route("/<string:nomTable>/<string:nomAttribut>")
class Attribut(Resource):
    def get(self,nomTable,nomAttribut):
        """
        Faire un select par rapport a un attribut
        """
        li=[nomAttribut]
        return selectAttribut(login,NameDB,nomTable,li)
    def post(self,nomTable,nomAttribut):
        """
        Ajouter un attribut dans une tablle
        """
        data=request.get_json()
        return AddAttribut(login,NameDB,nomTable,nomAttribut,data) 
    def delete(self,nomTable,nomAttribut):
         
        return DropAttribut(login,NameDB,nomTable,nomAttribut)
    def put(self,table,nomTable,nomAttribut):
        data=request.get_json()
        return  AlterAlterAttribut(login,NameDB,nomTable,nomAttribut,data)

@db_RenameDB.route("/<string:NomDB>")
class RenameTable(Resource):
    def put(self,NomDB):
        """
        rennome le nom de la base de données
        """
        global NameDB
        tmp=NomDB+'.json'
        if renameDB(login,NameDB,tmp)==True:
            NameDB=NomDB+".json"
            return "Modification reussit :)"
        return "Erreur de modification (:"
@db_select.route("/<string:NomTable>")
class select(Resource):
    def get(self,NomTable):
        """
        returne la liste des informations d'une table
        """
        return selectTout(login,NameDB,NomTable)
@db_select.route("/<string:NomTable>/<string:attribut>/<string:value>")
class selectwhere(Resource):
    def get(self,NomTable,attribut,value):
        """
        returne liste des informations par rapport a un attribut en fonction d'une valeur bien definis
        """
        return selectToutWhere(login,NameDB,NomTable,attribut,value)

     
    
@ns_Table.route("/<string:NomTable>")
class TablePlusAttribut(Resource):
    def get(self,NomTable):
        """
        return la liste des information de la table
        """
        return selectTout(login,NameDB,NomTable)
    def post(self,NomTable):
        """
        Add une nouvelle table dans la base de données
        """
        data=request.get_json()
        return CreateTable(login,NameDB,NomTable,data) 
    
    def delete(self, nomTable):
        
        DropTable(login,nomTable)
        return "Suppression de la table reussit"
"""        
@ns_DBs.route("/<string:title>")
class DBsList(Resource):
    def get(self,title):
        
        return showDataBase(login,title)
    def post(self,title):
       
        CreateDB(login,title)
        return "Creation de la base de données reussit"
    def delete(self, title):
        
        DropDB(title)
        return "Suppression de la base de données reussit"
"""
@db_SelectionDB.route("/<string:NomDB>")
class USEDB(Resource):
    def get(self,NomDB):
        global NameDB
        tmp=""+NomDB+".json"
        if isAbility(login,tmp,'r')==True :
            NameDB=NomDB+".json"
            return "Selection de la base de données %s reussit"% NomDB
        else:
            return isAbility(login,NameDB,'r')
            
    def delete(self, NomDB):
        global NameDB

        if NameDB!=None:
            return "deconnexion reussit"
        return "Impossible vous devez vous connecter à une base de données d'abord"

@db_Connexion.route("/<string:identifiant>/<string:MotDePasse>")
class Connected(Resource):
    def get(self,identifiant,MotDePasse):
        if isHere(identifiant,MotDePasse)==True:
            global login
            global password
            login=identifiant
            password=MotDePasse
            return "Identification reussit :) %s" %login   
        else:
            return "Login ou mot de passe incorrecte"

        return NameDB
    def delete(self,identifiant,MotDePasse):
        global NameDB
        if NameDB!=None:
            login=identifiant
            password=MotDePasse
            return "Deconnxion reussit :) %s" %NameDB   
        else:
            return "Pour vous déconnectez il va falloir vous connecter d'abord"
app.run(debug=True,port= 8887, host= '127.0.0.1')
