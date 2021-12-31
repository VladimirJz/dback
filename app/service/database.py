#!/usr/bin/python
#from pynotifier import Notification
from sys import setrecursionlimit
import pyodbc
import random

class connection():
    def __init__(self,server,user,passw):
        '''Server:IP or hostname | user: User | passws: password'''
        self._driver ="ODBC Driver 17 for SQL Server" #add logic for OS driver
        self._server=server
        self._user=user
        self._passw=passw
        #self._database=''

       #Users
    @property
    def driver(self):
         return self._driver
    
    @driver.setter
    def driver(self,value):
        self._driver = "ODBC Driver 17 for SQL Server"

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
        print(db_constring)
        return db_constring
    
    def get_connection(self):
        db_strcon= self.get_stringconnection()
        db_connection=pyodbc.connect(db_strcon)  
        print('Success Connection to ' + self._database )       
        return db_connection


class admin_connection(connection):
    def __init__(self,server,user,passw,job_id):
        self._current_job = job_id
        self._database='dba'
        super().__init__(server,user,passw)
    
    @property
    def current_job(self):
        return self._current_job   






class transfer_job():
    def __init__(self,repo,source,target):
        print('initialize')
        self._job   =repo.current_job
        self._repo  =repo.get_connection() # repo es una connexión
        self._target=source.get_connection() # cambiar a targets

    def generate_data_scripts(self):
        print('Tables whit filters:')
        sql=('select [Name],[Schema],'
            '[Column],[FilterType],[LowerValue],[UpperValue],[ValuesDataType],'
            '[StepBy],[Table_id] '
            'from catalog_tables ct inner join (deploy_tablefilters tf '
            'inner join  deploy_tablefilters_Job tfj on tf.id=tfj.tablefilters_id) '
            'on ct.id=tf.Table_id '
            'where tfj.jobs_id=1')

        db=dbhandler(self._repo)
        #con=self.repo.get_connection()
        #print(con)
        filtered_tables=db.get_resulset(self._repo,sql)
        print(filtered_tables)


    def ofuscate_scripts(self):
        print('Ofuscate tables')
        sql=('select [Name],[Schema],'
            '[Column],[FilterType],[LowerValue],[UpperValue],[ValuesDataType],'
            '[StepBy],[Table_id] '
            'from catalog_tables ct inner join (deploy_tablefilters tf '
            'inner join  deploy_tablefilters_Job tfj on tf.id=tfj.tablefilters_id) '
            'on ct.id=tf.Table_id '
            'where tfj.jobs_id=1')
        # obtener parametros
        
        schema='dbo'
        field='Nombre'
        table='Empleados'
        field_id='Id_emp'
        sample=40
        target=dbhandler(self._target)
        repo=dbhandler(self._repo,self._job)
        rows=target.row_count(table)
        portion=rows//sample
        print(''+ str(rows))
        random_names=target.get_random(sample,field,table)
        #print(random_names)
        jump=0
        first=0
        block=0
        scripts=[]
        for i, name in enumerate(random_names):
            block+=portion

            jump = random.randint(portion,block)
            first=block-random.randint(jump,block)
            first=block
            last=random.randint(first,block)+jump
            if i==0 :
                first=0

            # ADD: for_update()
            sql="UPDATE " + table  + " set " + field  + "= '"+ name +"' WHERE " + field_id + ">=" + str(first) + " AND " + field_id + "<=" + str(last) + ";"
            scripts.append(sql)
        print (scripts)
        repo.add(scripts)

            






class dbhandler():
  
    
    def __init__(self,connection,current_job=None):
        self._current_job=current_job
        self._connection=connection
        pass


    def read_field(self,sql):
        #self._connection.execute
        value = self._connection.execute(sql).fetchval()
        return value
    
    def get_list(self,sql):
        #list=self._connection.execute(sql).fetchall()
        list = [item[0] for item in self._connection.execute(sql).fetchall()]

        return list
        #self._connection

        #     cursor=db.cursor()
        # cursor.execute(sql)
        # records=cursor.fetchall

    def add(self,scripts):
        sql="select coalesce(max([Order]),0)Last from deploy_jobscripts where Job_id=" + str(self._current_job)
        last_step=self.read_field(sql)
        count=len(scripts)
        order_list=[]
        for i in range(last_step, last_step+count):
            order_list.append(i)
        print(order_list)

        pass

    def row_count(self,table):
        sql='SELECT COUNT(*) FROM ' + table
        rows=self.read_field(sql)
        return  rows

    def get_random(self,rows,field,table):
        sql='SELECT TOP ' + str(rows)  + ' ' + field + ' FROM ' + table + ' ORDER BY  NEWID()'
        list= self.get_list(sql)
        return list
     







    def get_resulset(self,connection,sql):
        '''return a list of dic's'''
        # db=self.open(server)
        db=connection
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








    def executer(self,server,sql):
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

class util():
    def list(self):
        pass