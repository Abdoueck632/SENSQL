from pyparsing import (
    Word,
    delimitedList,
    Optional,
    Literal,
    Group,
    alphas,
    alphanums,
    Forward,
    oneOf,
    Combine,
    quotedString,
    infixNotation,
    opAssoc,
    restOfLine,
    CaselessKeyword,
    pyparsing_common as ppc,
)

        
def usedb(query):

# define SQL tokens
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


    
    return simpleSQL.parseString(query)
    
def createUser(query):
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


    
    return simpleSQL.parseString(query)

def createTable(query):
    # define SQL tokens
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



    return simpleSQL.parseString(query)

def createDB(query):

    # define SQL tokens
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


    query = input(">>>> ")
    return simpleSQL.parseString(query)

def connexion(query):
    # define SQL tokens
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

    return simpleSQL.parseString(query)
   
