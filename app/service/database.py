#!/usr/bin/python
#from pynotifier import Notification
from sys import setrecursionlimit
import pyodbc

class workspace():
    def __init__(self):
          self._server =''
          self._target=''
          self._source=''

 #get-set       
    @property
    def server(self):
         return self._server 

    @server.setter
    def server(self,value):
        self._server = value
        
    @property
    def target(self):
         return self._target 

    @target.setter
    def target(self,value):
        self._target = value

    @property
    def source(self):
         return self._source 

    @source.setter
    def source(self,value):
        self._source = value
    #Users
    @property
    def user(self):
         return self._user
    @property
    def passw(self):
         return self._passw      


class stringconnection():
    def __init__(self):
        self._driver =''
        self._server=''
        self._user=''
        self._passw=''
        self._database=''

       #Users
    @property
    def driver(self):
         return self._driver
    
    @driver.setter
    def driver(self,value):
        self._driver = "{SQL Server Native Client 11.0}"

    @property
    def server(self):
         return self._server   
    
    @server.setter
    def server(self,value):
        self._server = value
    
    @property
    def user(self):
         return self._user
    @user.setter
    def user(self,value):
        self._user = "sa"

    @property
    def passw(self):
         return self._passw  
    @passw.setter
    def passw(self,value):
        self._passw = "#1Qazse4"
    
    @property
    def database(self):
         return self._database 
    @database.setter
    def database(self,value):
        self._database = value



    def get_stringconnection(self):
        db_constring=("Driver="+ self._driver + ";"
                "Server="+  self._server +";"
                "Database="+ self._database + ";"
                "UID=" + self.user + ";"
                "PWD="+ self._passw +";")
        return db_constring

class repository():




        

    def stringconection(self,workspace):
        driver="Driver={'SQL Server Native Client 11.0}"
        server="Server="+ workspace.server 
        user="UID=" + workspace.user
        user="PWD=" + workspace.passw


        return workspace.target
        

    def open(self,server):
        if server=='IEEPO':
            db_constring=("Driver={SQL Server Native Client 11.0};"
                        "Server=172.16.20.3;"
                        "Database=dba;"
                        "UID=sa;"
                        "PWD=#1Qazse4;")
        else: 
            db_constring=("Driver={SQL Server Native Client 11.0};"
                        "Server=172.16.20.3;"
                        "Database=DESARROLLO;"
                        "UID=sa;"
                        "PWD=#1Qazse4;")
        db_connection=pyodbc.connect(db_constring)         
        return db_connection


    def get_resulset(self,server,sql):
        '''return a list of dic's'''
        db=self.open(server)
        cursor=db.cursor()
        cursor.execute(sql)
        records=cursor.fetchall
        dataset = []
        column_names = [column[0] for column in cursor.description ]
        #print(records)
        #print(column_names)
        for row in cursor:
            #print(row.SCRIPT)
            dataset.append(dict(zip(column_names,row)))
        # for record in records:
        #     insertObject.append( dict( zip( column_names , record ) ) )
        cursor.close()
        return dataset

    def execute(self,server,sql):
        db=self.open(server)
        cursor=db.cursor()
        if(cursor.execute(sql)):
            success=True
        else:
            success=False
        cursor.commit()
        cursor.close()
        return success

    def get_table_columns(self,server,database,table):
        i=self.info()
        db=self.open(server)
        cursor=db.cursor()

#         Var_SQL="EXEC BACKUPUPDATE ?,?,?,?,?,?,?,?"
#         cursor= db_conexion.cursor()
#         params=(i.column_names)
#         if(cursor.execute(Var_SQL,params)):
#         x=1
#         return x
# class info():
#     column_names="SELECT STRING_AGG(concat('[',COLUMN_NAME,']'),',') FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME =?  and TABLE_CATALOG=?"