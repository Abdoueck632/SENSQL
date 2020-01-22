import socket
from threading import Thread
from socketserver import ThreadingMixIn
from Base import *
from Recuperation import *
usedb="use database"
createTable="create table"
createUser="create user"
createDB="create database"
connexion="mysql -u"
insertion="insert into"
dropTable="drop table"
deleteAttr="delete"
NameDB=""
login=""
password=""
# Multithreaded Python server : TCP Server socket Thread Pool
class ClientThread(Thread):

    def __init__(self, ip, port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        print("[+] New server socket thread started for " + ip + ":" + str(port))
    
    def run(self):
        while True:
            data = conn.recv(2048)
            mess=data.decode()
            
            print("Server received data: ",mess)
            mss=saCommence(mess)
            mss=str(mss)
            if mess == "exit": 
                print("quiting...")
                break 

            
            conn.send(mss.encode())


print('Running...')
print('\n')

# Multithreaded Python server : TCP Server socket Thread Stub
TCP_IP = '127.0.0.1'
TCP_PORT = 8888
BUFFER_SIZE = 20 

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpServer.bind((TCP_IP, TCP_PORT))
threads = []

def saCommence(req):
   
    if req.startswith(usedb):
        global login
        if login!="" :
            
            useStmt = Forward()
            USE, DATABASE = map(
                CaselessKeyword, "use database".split()
            )

            ident = Word(alphas).setName("identifier")
            databaseName = delimitedList(ident).setName("database")
            databaseName.addParseAction(ppc.upcaseTokens)
            #tableNameList = Group(delimitedList(tableName))


            # define the grammar
            useStmt <<= (
                USE
                + DATABASE
                + databaseName("use")
                + Literal(';')
            )

            simpleSQL = useStmt

            # define Oracle comment format, and ignore them
            oracleSqlComment = "--" + restOfLine
            simpleSQL.ignore(oracleSqlComment)


            
            resultat = simpleSQL.parseString(req)
            tmp=""+resultat.use[0]+".json"
            red=tmp.lower()
            print("selection echoué", red)
            if isAbility(login,red,'r')==True :
                global NameDB
                NameDB=red
                return "connexion reussit >>>> DATABASE CHANGED : ", resultat.use[0]
               
            else:
                print("selection echoué", tmp)
                return "Vous n'etes pas abilité à modifier"
        else:
            print("Veuillez vous connecter avant de manipuler le SGBD")
            return "Veuillez vous connecter avant de manipuler le SGBD"
        
    if req.startswith(createTable):
        if  NameDB!="":    
            createStmt = Forward()
            CREATE, TABLE, INT, DATE, TIME, CHAR, VARCHAR, FLOAT = map(
                CaselessKeyword, "create table int date time char varchar float".split()
            )

            ident = Word(alphas).setName("identifier")
            #columnName = delimitedList(column)
            #columnName.addParseAction(ppc.upcaseTokens)
            #columnNameList = Group(delimitedList(columnName))
            tableName = delimitedList(ident, ".", combine=True).setName("table")
            tableName.addParseAction(ppc.upcaseTokens)
            #tableNameList = Group(delimitedList(tableName))

            intValue = ppc.signed_integer()
            INTEGER = INT
            varcharType = Combine(VARCHAR + "(" + intValue + ")")



            columnType = (
                INT | INTEGER | TIME | DATE | varcharType | CHAR | FLOAT
            )

            columnValue = Group(
                ident + columnType

            )

            columnNameList = Group(
                delimitedList(columnValue, ",")
            )


            # define the grammar
            createStmt <<= (
                CREATE
                + TABLE("create")
                + tableName("table")
                + Literal("(")
                + columnNameList("column")
                + Literal(")")
                + Literal(';')
            )

            simpleSQL = createStmt

            # define Oracle comment format, and ignore them
            oracleSqlComment = "--" + restOfLine
            simpleSQL.ignore(oracleSqlComment)


            
            resultat = simpleSQL.parseString(req)
            nomtable=resultat.table.lower()
            Attribut=resultat.column
            dictio=dict()
            for att in resultat.column:
                dictio[att[0]]=[att[1],'']
            CreateTable(login,NameDB,nomtable,dictio)
            print("Creation : ", resultat.create)
            print("Table : ", resultat.table)
            print("Attribut : ", resultat.column)
            return "Creation de la table %s reussit "% nomtable
        else:
            print("Désolé vous n'etes connecter ou la base de données n'est pas selectionné")
            return "Désolé vous n'etes connecter ou la base de données n'est pas selectionné"
    if req.startswith(createUser):
        if login=='admin':   
            userStmt = Forward()
            CREATE, USER, IDENTIFIED, BY = map(
                CaselessKeyword, "create user identified by".split()
            )

            ident = Word(alphas).setName("identifier")
            userName = delimitedList(ident).setName("user")
            userName.addParseAction(ppc.upcaseTokens)
            #tableNameList = Group(delimitedList(tableName))

            intValue = ppc.signed_integer()

            pwdValue = Group("passer" + intValue)


            # define the grammar
            userStmt <<= (
                CREATE
                + USER
                + userName("user")
                + IDENTIFIED
                + BY
                + pwdValue("pwd")
                + Literal(';')
            )

            simpleSQL = userStmt

            # define Oracle comment format, and ignore them
            oracleSqlComment = "--" + restOfLine
            simpleSQL.ignore(oracleSqlComment)


            
            resultat = simpleSQL.parseString(req)
            mdp=""+resultat.pwd[0]+str(resultat.pwd[1])
            login=str(resultat.user[0])
            user='admin'
            if user=='admin':
                try:
                    with open('users.json', 'r') as fp:
                        dic = json.load(fp)
                except Exception as error:
                    dic=dict()
                tmp=dict()
                tmp['login']=login
                tmp['password']=mdp
                tmp['listeDB']=""
                dic[login]=tmp
                with open('users.json', 'w') as write_file:
                        write_file.write(json.dumps(dic, indent=4))
                return  "Creation de l'utlisateur %s reussit" % login
            else:
                return "Désolé seul l'administrateur peut creer un utilisateur"
        else:
            print("Seule l'administrateur a le droit de creer d'utilisateur")
            return "Seule l'administrateur a le droit de creer d'utilisateur"
    if req.startswith(createDB):
        if login!="" :
                      
            dbStmt = Forward()
            CREATE, DATABASE = map(
                CaselessKeyword, "create database".split()
            )

            ident = Word(alphas).setName("identifier")
            databaseName = delimitedList(ident).setName("database")
            databaseName.addParseAction(ppc.upcaseTokens)
            #tableNameList = Group(delimitedList(tableName))


            # define the grammar
            dbStmt <<= (
                CREATE
                + DATABASE
                + databaseName("db")
                + Literal(';')
            )

            simpleSQL = dbStmt

            # define Oracle comment format, and ignore them
            oracleSqlComment = "--" + restOfLine
            simpleSQL.ignore(oracleSqlComment)


            
            resultat = simpleSQL.parseString(req)
            tmp=""+resultat.db[0].lower()+".json"
            CreateDB(login,tmp)
            print("DATABASE : ", resultat.db[0].lower())
            return "Creation reussit :)"
        else:
            print("Veuillez vous connectez avant :)")
            return "Veuillez vous connectez avant :)"
    if req.startswith(connexion):
        stmt = Forward()
        MYSQL, U, P = map(
            CaselessKeyword, "mysql u p".split()
        )

        ident = Word(alphas).setName("identifier")
        userName = delimitedList(ident).setName("user")
        userName.addParseAction(ppc.upcaseTokens)


        intValue = ppc.signed_integer()
        pwdValue = quotedString()



        # define the grammar
        stmt <<= (
            MYSQL
            + Literal('-')
            + U
            + userName("user")
            + Literal('-')
            + P
            + pwdValue("pwd")
            + Literal(';')
        )

        simpleSQL = stmt

        # define Oracle comment format, and ignore them
        oracleSqlComment = "--" + restOfLine
        simpleSQL.ignore(oracleSqlComment)

        
        resultat = simpleSQL.parseString(req)
        resultat.pwd = resultat.pwd.replace("\"","")
        tmp=str(resultat.user[0])
        tmp=tmp.lower()
        print("User : ", tmp)
        print("Pwd : ", str(resultat.pwd))
        mdp=str(resultat.pwd)
        if isHere(tmp,mdp)==True:
            
            tmp=resultat.user[0]
            tmp=str(resultat.user[0])
            login=tmp.lower()
            print(">>> Bienvenu sur Mysql...")
            return ">>> Bienvenu sur Mysql...",login

            print("User : ", resultat.user[0])
            print("Pwd : ", str(resultat.pwd))

        else:
            print("login ou mot de passe incorrecte")
            return "login ou mot de passe incorrecte"
    if req.startswith(insertion):
        if login!="":
           
            insertStmt = Forward()
            INSERT, INTO, VALUES, = map(
                CaselessKeyword, "insert into values".split()
            )

            ident = Word(alphas).setName("identifier")
            tableName = delimitedList(ident, ".", combine=True).setName("table")
            tableName.addParseAction(ppc.upcaseTokens)

            intValue = ppc.signed_integer()
            realValue = ppc.real()
            valueType = intValue | realValue | quotedString()
            valeur = Group("(" + delimitedList(valueType, ",") + ")")
            valeurMulti = delimitedList(valeur, ",")

            insertStmt <<= (
                INSERT

                + INTO
                + tableName("table")
                + VALUES
                + valeurMulti("valeur")
                + Literal(";")
            )

            simpleSQL = insertStmt

            oracleSqlComment = "--" + restOfLine
            simpleSQL.ignore(oracleSqlComment)


            resultat = simpleSQL.parseString(req)

            nomtable=resultat.table.lower()
            for x in resultat.valeur:
                print(x)
                tab=[]
                for r in x:
                    if r==x[0] or r==x[len(x)-1]:
                        pass
                    else:
                        s=str(r)
                        tab.append(s)
                AddValues(login,NameDB,nomtable,tab)        
            print("Table :", resultat.table)
            print("Values :", resultat.valeur)
            print("Ajout reussit :)")
            return "Ajout reussit :)"
        else:
            print("Veuillez vous connecter d'abord")
            return "Veuillez vous connecter d'abord"

    if req.startswith(dropTable):
        # define SQL tokens
        if login!="" :
            
            dropStmt = Forward()
            DROP, TABLE = map(
                CaselessKeyword, "drop table".split()
            )


            ident = Word(alphas).setName("identifier")
            tableName = delimitedList(ident, ".", combine=True).setName("table")
            tableName.addParseAction(ppc.upcaseTokens)
            #tableNameList = Group(delimitedList(tableName))

            # define the grammar
            dropStmt <<= (
                DROP
                + TABLE
                + tableName("table")
                + Literal(';')
            )

            simpleSQL = dropStmt

            # define Oracle comment format, and ignore them
            oracleSqlComment = "--" + restOfLine
            simpleSQL.ignore(oracleSqlComment)


            
            resultat = simpleSQL.parseString(req)
            nomtable=resultat.table.lower()
            DropTable("admin",'teste.json',nomtable)
            print("Supprimer : ", resultat.table)
            return "suppression de la table %s reussit "% resultat.table
    else:
        print("Veuillez vous connecter d'abord")
        return "Veuillez vous connecter d'abord"
    if  req.startswith(deleteAttr):
        # define SQL tokens
        if login!="":   
            delStmt = Forward()
            DELETE, FROM, WHERE, AND = map(
                CaselessKeyword, "delete from where and".split()
            )

            ident = Word(alphas).setName("identifier")
            columnName = delimitedList(ident, ".", combine=True).setName("column")
            columnName.addParseAction(ppc.upcaseTokens)
            #columnNameList = Group(delimitedList(columnName))
            tableName = delimitedList(ident, ".", combine=True).setName("table")
            tableName.addParseAction(ppc.upcaseTokens)
            tableNameList = Group(delimitedList(tableName))

            oper = oneOf("= != < > >= <= like eq ne lt le gt ge lk", caseless=True)
            realNum = ppc.real()
            intNum = ppc.signed_integer()

            columnRval = (
                realNum | intNum | quotedString
            )
            whereCondition = Group(
                (columnName + oper + columnRval)

            )

            # define the grammar
            delStmt <<= (
                DELETE
                + FROM
                + tableName("table")
                + WHERE
                + whereCondition("where")
                + Literal(";")

            )

            simpleSQL = delStmt

            # define Oracle comment format, and ignore them
            oracleSqlComment = "--" + restOfLine
            simpleSQL.ignore(oracleSqlComment)


            resultat = simpleSQL.parseString(req)
            nomtable=str(resultat.table)
            nomtable=nomtable.lower()
            attr=str(resultat.where[0])
            attr=attr.lower()
            valu=str(resultat.where[len(resultat.where)-1])

            DropValues('admin','teste.json',nomtable,attr,valu)
            #print("Colonnes :", resultat.col)
            print("Tables :", resultat.table)
            print("Where :", resultat.where)
            print("suppression reussit :)")
            return  "suppression reussit :)"
        else:
            print("Veuillez vous connecter d'abord")
            return "Veuillez vous connecter d'abord"
    else:
        return "Commande introuvable"
while True:
    tcpServer.listen(4)
    print("Multithread Python server : Waiting for connections from TCP clients...")
    (conn, (ip, port)) = tcpServer.accept()
    newthread = ClientThread(ip, port)
    newthread.start()
    threads.append(newthread)

tcpServer.close()
for t in threads:
    t.join()
