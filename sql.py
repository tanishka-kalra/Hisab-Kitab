import psycopg2


def  make_connection():
    connection = psycopg2.connect(
    dbname="Sample",
    user="postgres",
    password="tanu@091710",
    host="localhost",
    port="5432"
    )
    return connection

def find_a_record(name):
    connection = make_connection()
    cursor=connection.cursor()
    sql_query="SELECT * FROM USER WHERE name = %s"
    try : 
        cursor.execute(sql_query,(name,))
        data=cursor.fetchall()
    except:
        return "An error Occured while finding a record"
    finally:
        cursor.close()
        connection.close()

def add_record(data):
    connection = make_connection()
    cursor=connection.cursor()
    data_tuple=tuple(data)
    sql_query='''INSERT INTO "USER"(name,mobile) VALUES(%s,%s)'''
    try:
        cursor.execute(sql_query,data_tuple)
        return (f"{data_tuple[0]} User Entered Succesfully")
    except:
        return "An error Occured while Inserting a User , Maybe the user already exist"
    finally:
        connection.commit()
        cursor.close()
        connection.close()
    
def getAllData(data):
    dt=tuple(data)
    connection = make_connection()
    cursor=connection.cursor()
    
    sql_query=''' WITH abcd AS (
  SELECT 
    "TRANSACTION".trans_id, 
    "TRANSACTION".id AS transaction_id,  -- Rename to avoid conflict
    "USER".name, 
    "USER".mobile, 
    "TRANSACTION".location, 
    "TRANSACTION".date, 
    "TRANSACTION".notes, 
    "TRANSACTION".status,
    "TRANSACTION".amount, 
    row_number() OVER (ORDER BY "TRANSACTION".trans_id DESC) AS ROW_NUM
  FROM 
    "TRANSACTION"
  INNER JOIN 
    "USER" 
  ON 
    "USER".id = "TRANSACTION".id
)
SELECT 
   
  abcd.transaction_id,  -- Use the renamed transaction_id
  abcd.trans_id,
  abcd.name, 
  abcd.amount,
  abcd.mobile, 
  abcd.location, 
  abcd.date, 
  abcd.notes, 
  abcd.status 
FROM 
  abcd
  WHERE row_num >= %s and row_num<= %s;
  '''

    try:
        print(sql_query)
        cursor.execute(sql_query,dt)
        data = cursor.fetchall()
        return data
    except:
        return "An error occured at return the entire data"
    finally:
        cursor.close()
        connection.close()
def find_a_email(email):
    connection = make_connection()
    cursor=connection.cursor()
    sql_query='''SELECT * FROM "USER_CRED" WHERE email = %s'''
    try : 
        print(sql_query)
        cursor.execute(sql_query,(email,))
        data=cursor.fetchall()
        print(data)
        print(bool(data))
        return bool(data)
        
    except:
        return "An error Occured while finding a email id record"
    finally:
        cursor.close()
        connection.close()

def viewOnUserData(names):
    connection = make_connection()
    cursor=connection.cursor()
    sql_query=''' SELECT  name , amount, location, mobile, date, notes, status
        FROM "TRANSACTION"
        RIGHT JOIN "USER" ON "USER".id = "TRANSACTION".id
        WHERE name = %s
        ORDER BY "TRANSACTION".Date
        '''
    try:
        for i in names :
            cursor.execute(sql_query,(i,))
        data=cursor.fetchall()
        return data
    except:
        return "An error Occursed while returning data based on Name filter"
    finally:
        cursor.close()
        connection.close()
    

def dataforedit(id):
    print(id)
    connection = make_connection()
    cursor=connection.cursor()
    sql_query=''' SELECT  "TRANSACTION".trans_id , name , amount,"USER".mobile , location,  date, notes, status
        FROM "TRANSACTION"
        RIGHT JOIN "USER" ON "USER".id = "TRANSACTION".id
        WHERE "TRANSACTION".trans_id = %s
        ORDER BY "TRANSACTION".Date
        '''
    try:
        print(sql_query)
        cursor.execute(sql_query,(id,))
        data=cursor.fetchall()
        print(data)
        return data
    except:
        return "An error Occursed while returning data based on Name filter"
    finally:
        cursor.close()
        connection.close()

def updateInDbsql(data):
    connection = make_connection()
    cursor=connection.cursor()
    data_tuple=tuple(data)
    sql_query='''UPDATE "TRANSACTION"
             SET notes = %s, status = %s
           WHERE trans_id = %s
            '''
    try:
        cursor.execute(sql_query,data_tuple)
        return "Data Update Successfully"
    except:
        return "An Error Occured while updating your data"
    finally:
        connection.commit()
        cursor.close()
        connection.close()

    
def addinTransaction(dataList):
    connection = make_connection()
    cursor=connection.cursor()
    datatuple = tuple(dataList)
    sql_query='''INSERT INTO "TRANSACTION"(id,amount,location,date,notes,status) VALUES(%s,%s,%s,%s,%s,%s)'''
    try:
        cursor.execute(sql_query,datatuple)
        return "Details entered successfully"
    except:
        return "An error Occured while Inserting the pre-existing user data"
    finally:
        connection.commit()
        cursor.close()
        connection.close()
    
def updateIntransaction(data):
    connection = make_connection()
    cursor=connection.cursor()
    datatuple=tuple(data)
    try:
        sql_query='''UPDATE "TRANSACTION"
             SET NOTES = %s, status = %s
           WHERE id = %s AND date = %s;
            '''
        cursor.execute(sql_query,datatuple)
        return "Record Updated Successfully"
    except:
        return "An error Occured while Updating the Data"
    finally:
        connection.commit()
        cursor.close()
        connection.close()
def registerUser(cred):
    connection = make_connection()
    cursor=connection.cursor()
    datatuple=tuple(cred)
    try:
        sql_query='''INSERT INTO "USER_CRED"(firstname, lastname,email , password) VALUES(%s,%s,%s,%s)'''
        cursor.execute(sql_query,datatuple)
        return "USER Registered Successfully"
    except:
        return "An error Occured while registering the user"
    finally:
        connection.commit()
        cursor.close()
        connection.close()
def getAllNames():
    connection = make_connection()
    cursor=connection.cursor()
    sql_query='''SELECT id , name FROM "USER" ORDER BY name'''
    try:
        cursor.execute(sql_query)
        data=cursor.fetchall()
        return data
    except:
        return "An error Occured Fetching the List of Names"
    finally:
        cursor.close()
        connection.close()
    
def getDateData(date):
    connection = make_connection()
    cursor=connection.cursor()
    sql_query='''
        SELECT "USER".id, "TRANSACTION".trans_id, name, amount, "USER".mobile, location, date, notes, status
        FROM "TRANSACTION"
        INNER JOIN "USER" ON "TRANSACTION".id = "USER".id
        WHERE "TRANSACTION".date = %s;
    '''
    try:
        cursor.execute(sql_query,(date,))
        data=cursor.fetchall()
        return data
    except:
        return "An error Occured Fetching the List of Names"
    finally:
        cursor.close()
        connection.close()

def viewOnFilter(data):
    print(data)
    connection = make_connection()
    cursor=connection.cursor()
    id=data['id']
    date=data['date']
    status=data['status']
    lower=data['lower']
    upper=data['upper']
    
    lst=[]
    # sql_query='''SELECT "USER".id, "TRANSACTION".trans_id, name, amount, "USER".mobile, location, date, notes, status
    #     FROM "TRANSACTION"
    #     INNER JOIN "USER" ON "TRANSACTION".id = "USER".id '''
    # if name or date or status : sql_query+='''WHERE '''
    # if name!='':
    #     sql_query+='''"USER".id = %s AND '''
    #     lst.append(int(name))
    # if date!='':
    #     sql_query+='''date = %s AND '''
    #     lst.append(date)
    # if status!='':
    #     sql_query+='''status=%s '''
    #     lst.append(status)
    
    # sql_query=sql_query[0:-4]
    # print(sql_query)
    # data_tuple=tuple(lst)
    # print(data_tuple)

    # cursor.execute(sql_query,data_tuple)
    # data=cursor.fetchall()
    # print(data)
    
    # cursor.close()
    # connection.close()
    sql_query=''' WITH abcd AS (
  SELECT 
    "TRANSACTION".trans_id, 
    "TRANSACTION".id AS transaction_id,  -- Rename to avoid conflict
    "USER".name, 
    "USER".mobile, 
    "TRANSACTION".location, 
    "TRANSACTION".date, 
    "TRANSACTION".notes, 
    "TRANSACTION".status,
    "TRANSACTION".amount, 
    row_number() OVER (ORDER BY "TRANSACTION".trans_id DESC) AS ROW_NUM
  FROM 
    "TRANSACTION"
  INNER JOIN 
    "USER" 
  ON 
    "USER".id = "TRANSACTION".id
    WHERE'''
    if id!='':
        sql_query+='''"TRANSACTION".id = %s AND '''
        lst.append(int(id))
    if date!='':
        sql_query+='''date = %s AND '''
        lst.append(date)
    if status!='':
        sql_query+='''status=%s AND;'''
        lst.append(status)
    sql_query=sql_query[0:-4]
    sql_query+=')'
    sql_query+='''SELECT 
   
  abcd.transaction_id,  -- Use the renamed transaction_id
  abcd.trans_id,
  abcd.name, 
  abcd.amount,
  abcd.mobile, 
  abcd.location, 
  abcd.date, 
  abcd.notes, 
  abcd.status 
FROM 
  abcd
  WHERE row_num >= %s and row_num<= %s; '''

  
    # if id!='':
    #     sql_query+='''transaction_id = %s AND '''
    #     lst.append(int(id))
    # if date!='':
    #     sql_query+='''date = %s AND '''
    #     lst.append(date)
    # if status!='':
    #     sql_query+='''status=%s AND;'''
    #     lst.append(status)
    # sql_query=sql_query[0:-4]
    lst.append(lower)
    lst.append(upper)
    try:
        print(sql_query)
        print(lst)
        cursor.execute(sql_query,lst)
        data=cursor.fetchall()
        return data
    except:
        return "An error occured while returning data based on filter"
    finally:
        cursor.close()
        connection.close()

    
def authenticate(data):
    email=data[0]
    password=data[1]
    print("query for email" , email)
    print("query for password", password)
    connection = make_connection()
    cursor=connection.cursor()
    sql_query='''
        SELECT password FROM "USER_CRED" WHERE email = %s;
    '''

    print(sql_query)
    cursor.execute(sql_query,(email,))
    data=cursor.fetchall()
    if password==data[0][0]:
        return True
    else:
        return False

    cursor.close()
    connection.close()

def pagination(data):
    offset=data*100
    print(offset)
    connection = make_connection()
    cursor=connection.cursor()
    sql_query='''SELECT "USER".id, "TRANSACTION".trans_id, name, amount, "USER".mobile, location, date, notes, status
        FROM "TRANSACTION"
        INNER JOIN "USER" ON "TRANSACTION".id = "USER".id 
        LIMIT 25
        OFFSET %s;
        '''

    print(sql_query)
    cursor.execute(sql_query,(offset,))
    data=cursor.fetchall()
    cursor.close()
    connection.close()
    return data
    
