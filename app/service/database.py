#!/usr/bin/python
#from pynotifier import Notification
from sys import setrecursionlimit
import pyodbc
import random
#from datetime import timedelta, date,datetime
from datetime import datetime, timedelta

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
        self._target=target.get_connection() # cambiar a targets
        self._source=source.get_connection()

    
    def enable_insert_identity(self,table,value):
        sql="SET IDENTITY_INSERT " +  table  + " " 
        if(value==True):
            sql+=" ON"
        else:
            sql+=" OFF"

        return sql

    def clean_source(self,object_id):
        source=dbhandler(self._source)
        target=dbhandler(self._target)
        table=source.full_table_name(object_id,target._database)
        print("clean:"+table)
        sql="TRUNCATE TABLE " + table + ";"

        return sql
    def initialize(self):
        sql='delete  from deploy_jobscripts where Job_id=?'
        repo=dbhandler(self._repo)
        parameters=self._job
        if(repo.run(sql,parameters)):
            print('Cleaned')
        else:
            print('Error,  remove manually old scripts')
    
    def get_constraints(self,object_id):
        sql=("SELECT f.name,f.parent_object_id "
	        "FROM  sys.foreign_keys AS f INNER JOIN  sys.foreign_key_columns AS fc "
            "ON f.OBJECT_ID = fc.constraint_object_id "
	        "INNER JOIN  sys.tables t "
            "ON t.OBJECT_ID = fc.referenced_object_id "
	        "WHERE f.referenced_object_id = ?")
        parameters=object_id
        #print(sql)
        #get target active constrainsts
        #source=dbhandler(self._source)
        target=dbhandler(self._target)
        constraints=target.read_rows(sql,parameters)
        return constraints
        
    def disable_contraints(self,object_id,disable=True):
        constraints=self.get_constraints(object_id)
        source=dbhandler(self._source)
        target=dbhandler(self._target)
        scripts=[]
        for constraint in constraints:
            referenced_object_id=constraint.get('parent_object_id')
            name=constraint.get('name')
            table=source.full_table_name(referenced_object_id,target._database)
            alter="ALTER TABLE " + table + " "
            check="CHECK CONSTRAINT "  +  name + "; "
            no="NO"

            if(disable):
                script=alter + no + check
            else:
                script=alter + check
        
            scripts.append(script)
        sql = ' '.join([str(sentence) for sentence in scripts])
        #print(sql)
        return sql

    def create_target_database(self):
        scripts=[]
        scripts_types=[]
        DDL=1
        DML=2

        repo=dbhandler(self._repo,self._job)
        #schemas_script=self.create_schemas()
        #scripts.append(schemas_script)
        #scripts_types.append(DDL)

        # iterate
        sql=('select ct.[id],[ObjectID],[Name],[Schema],[Table_id] '
            'from catalog_tables ct inner join (deploy_tablefilters tf '
            'inner join  deploy_tablefilters_Job tfj on tf.id=tfj.tablefilters_id) '
            'on ct.id=tf.Table_id '
            'where ct.Status=1 '
            'and tfj.jobs_id=1')
 
        source=dbhandler(self._source)
        target=dbhandler(self._target)
        #print('reda')
        filtered_tables=repo.read_rows(sql)
        for table in filtered_tables:
            object_id=table.get('ObjectID')
            #print(object_id)
            create_script=self.create_table(object_id)
            scripts.append(create_script)
            scripts_types.append(DML)
            pass
        pass
        #print(scripts)
        repo.add(scripts,scripts_types)


        

    def generate_data_scripts(self):
        print('Tables whit filters:')
        sql=('select ct.[id],[ObjectID],[Name],[Schema],'
            '[Column],[FilterType],[LowerValue],[UpperValue],[ValuesDataType],'
            '[StepBy],[Table_id] '
            'from catalog_tables ct inner join (deploy_tablefilters tf '
            'inner join  deploy_tablefilters_Job tfj on tf.id=tfj.tablefilters_id) '
            'on ct.id=tf.Table_id '
            'where ct.Status=1 '
            'and tfj.jobs_id=1')
        dml=2
        ddl=1
        script_type=dml

        repo=dbhandler(self._repo,self._job)
        source=dbhandler(self._source)
        target=dbhandler(self._target)
    
        #con=self.repo.get_connection()
        #print(con)
        filtered_tables=repo.get_resulset(self._repo,sql)
        for filter in filtered_tables:
            scripts=[]
            scripts_types=[]
            table_id=filter.get('id')
            table=filter.get('Name')
            schema=filter.get('Schema')
            object_id=filter.get('ObjectID')
            FilterType=filter.get('FilterType')
            Column=filter.get('Column')
            Lower=filter.get('LowerValue')
            Upper=filter.get('UpperValue')
            DataType=filter.get('ValuesDataType')
            StepBy=filter.get('StepBy')
            #object_id=repo.object_id(table)
            print("== Working whit TABLE :" + table)
            full_table_name=source.full_table_name(object_id,target._database)
            constraints_script=self.disable_contraints(object_id)
            if(constraints_script):
                scripts.append(constraints_script)
            truncate_script=self.clean_source(object_id)
            #print (truncate_script)
            scripts.append(truncate_script)
            scripts_types.append(ddl)
            if(source.has_identity(object_id)):
                enable_insert_id=self.enable_insert_identity(full_table_name,True)
                scripts.append(enable_insert_id)
                scripts_types.append(ddl)
                
            column_names=source.get_columnnames(object_id)
            insert_into="INSERT INTO [" +schema + "].["+ table +"] (" + column_names + ")"
            from_table =" select " +  column_names  + " from " + source.full_table_name(object_id) + ""
            #print(FilterType,DataType)
            # begin=int(Lower)

            if(FilterType==3): # iterate
                # id stepby =1 then use ==
                if (DataType==3): #date
                    #begin=date(Lower)
                    begin=datetime.strptime(Lower,"%Y-%m-%d")
                    lastest=datetime.strptime(Upper,"%Y-%m-%d")
                    #print(type(begin))
                    #print(begin,lastest)
                    while begin <=lastest:
                        end=begin + timedelta(days=StepBy) 
                        if(end>lastest):
                            end=lastest
                        where=" where " + Column + ">=" + begin.strftime("'%Y-%m-%d'")+ " and " + Column + "<=" + end.strftime("'%Y-%m-%d'") + ";"
                        begin=end + timedelta(days=1)
                        sql=insert_into + from_table + where
                        scripts.append(sql)
                        scripts_types.append(dml)

                if(DataType==1):#int
                    begin=int(Lower)
                    lastest=int(Upper)
                    #print(begin,lastest)
                    while begin<=lastest:
                        end=begin+StepBy
                        if(end>lastest):
                            end=lastest
                        if(StepBy==1):
                            where=" where " + Column + "=" + str(begin) + ";"
                            begin+=StepBy
                        else:
                            where=" where " + Column + ">=" + str(begin) + " and " + Column + "<=" + str(end) + ";"
                            begin=end + 1
                        sql=insert_into + from_table + where
                        scripts.append(sql)
                        scripts_types.append(dml)
                        #print(sql)

            if(FilterType==0):#No Filter
                sql=insert_into + from_table
                scripts.append(sql)
                scripts_types.append(dml)

            if(source.has_identity(object_id)):
                disable_insert_id=self.enable_insert_identity(full_table_name,False)
                scripts.append(disable_insert_id)   
                scripts_types.append(ddl)
            #print(scripts)
            if(scripts):
                repo.add(scripts,scripts_types)


                
                #print(enable_insert_id)
                #print (column_names)
            
                
        print('done')
    def deploy_database(self):
        print('Deploy Start...')
        print('Running Scripts')
        target=dbhandler(self._target)
        repo=dbhandler(self._repo,self._job)
        sql=("select [Order],[Type] ,Script from deploy_jobscripts where Job_id=1"
            "order by [Order] asc")
        deploy_scripts=repo.read_rows(sql)
        for script in deploy_scripts:
            sql_script=script.get('Script')
            script_type=script.get('Type')
            print("stored script:"+ sql_script)
            print("<--")
            if(target.run(sql_script,type=script_type)):
                print('done..')
            else:
                print('===Error ! ==')


        

        

    def ofuscate_scripts(self):
        print('Ofuscate tables')
        sql=('select [Name],[Schema],'
            '[Column],[FilterType],[LowerValue],[UpperValue],[ValuesDataType],'
            '[StepBy],[Table_id] '
            'from catalog_tables ct inner join (deploy_tablefilters tf '
            'inner join  deploy_tablefilters_Job tfj on tf.id=tfj.tablefilters_id) '
            'on ct.id=tf.Table_id '
            'where tfj.jobs_id=1')
        dml=2
        script_type=dml
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
        #print(''+ str(rows))
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
        #print (scripts)
        if(scripts):
            repo.add(scripts,script_type)

      
    def create_schemas(self):
        sql=("SELECT  s.name "
            "FROM sys.schemas s "
            "INNER JOIN sys.sysusers u ON u.uid = s.principal_id "
            "where schema_id>4 and s.name not like 'db_%' "
            "ORDER BY s.schema_id;")
        
        scripts=[]
        source=dbhandler(self._source)
        schemas=source.read_rows(sql)
        for schema in schemas:
            schema_name=schema.get('name')
            create_schema="CREATE SCHEMA ["+ schema_name + "]  AUTHORIZATION dbo;"
            scripts.append(create_schema)
        sql = ' '.join([str(sentence) for sentence in scripts])
        return sql
      


    def create_table(self,object_id): 
        source=dbhandler(self._source)
        target=dbhandler(self._target)
        full_table_name=source.full_table_name(object_id,target._database)
        sql=(" SELECT 'CREATE TABLE ' +  '" + full_table_name  + "' + CHAR(13) + '(' + CHAR(13) + STUFF((   "
        "SELECT CHAR(13) + '    , [' + c.name + '] ' +    "
        "CASE WHEN c.is_computed = 1  "
        "THEN 'AS ' + OBJECT_DEFINITION(c.[object_id], c.column_id)  "
        "ELSE   "
        "CASE WHEN c.system_type_id != c.user_type_id   "
        "THEN '[' + SCHEMA_NAME(tp.[schema_id]) + '].[' + tp.name + ']'   "
        "ELSE '[' + UPPER(tp.name) + ']'   "
        "END  +   "
        "CASE   "
        "WHEN tp.name IN ('varchar', 'char', 'varbinary', 'binary')  "
        "THEN '(' + CASE WHEN c.max_length = -1   "
        "THEN 'MAX'   "
        "ELSE CAST(c.max_length AS VARCHAR(5))   "
        "END + ')'  "
        "WHEN tp.name IN ('nvarchar', 'nchar')  "
        "THEN '(' + CASE WHEN c.max_length = -1  " 
        "THEN 'MAX'   "
        "ELSE CAST(c.max_length / 2 AS VARCHAR(5))   "
        "END + ')'  "
        "WHEN tp.name IN ('datetime2', 'time2', 'datetimeoffset')   "
        "THEN '(' + CAST(c.scale AS VARCHAR(5)) + ')'  "
        "WHEN tp.name = 'decimal'  "
        "THEN '(' + CAST(c.[precision] AS VARCHAR(5)) + ',' + CAST(c.scale AS VARCHAR(5)) + ')'  "
        "ELSE ''  "
        "END +  "
        "CASE WHEN c.collation_name IS NOT NULL AND c.system_type_id = c.user_type_id   "
        "THEN ' COLLATE ' + c.collation_name  "
        "ELSE ''  "
        "END +  "
        "CASE WHEN c.is_nullable = 1   "
        "THEN ' NULL'  "
        "ELSE ' NOT NULL'  "
        "END +  "
        "CASE WHEN c.default_object_id != 0   "
        "THEN ' CONSTRAINT [' + OBJECT_NAME(c.default_object_id) + ']' +   "
        "' DEFAULT ' + OBJECT_DEFINITION(c.default_object_id)  "
        "ELSE ''  "
        "END +   "
        "CASE WHEN cc.[object_id] IS NOT NULL   "
        "THEN ' CONSTRAINT [' + cc.name + '] CHECK ' + cc.[definition]  "
        "ELSE ''  "
        "END +  "
        "CASE WHEN c.is_identity = 1   "
        "THEN ' IDENTITY(' + CAST(IDENTITYPROPERTY(c.[object_id], 'SeedValue') AS VARCHAR(5)) + ',' +   "
        "CAST(IDENTITYPROPERTY(c.[object_id], 'IncrementValue') AS VARCHAR(5)) + ')'   "
        "ELSE ''   "
        "END   "
        "END  "
        "FROM sys.columns c WITH(NOLOCK)  "
        "JOIN sys.types tp WITH(NOLOCK) ON c.user_type_id = tp.user_type_id  "
        "LEFT JOIN sys.check_constraints cc WITH(NOLOCK)   "
        "ON c.[object_id] = cc.parent_object_id   "
        "AND cc.parent_column_id = c.column_id  "
        "WHERE c.[object_id] = " + str(object_id) + "  "
        "ORDER BY c.column_id  "
        "FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 7, '      ') +   "
        "ISNULL((SELECT '  "
        ", CONSTRAINT [' + i.name + '] PRIMARY KEY ' +   "
        "CASE WHEN i.index_id = 1   "
        "THEN 'CLUSTERED'   "
        "ELSE 'NONCLUSTERED' "  
        "END +' (' + (  "
        "SELECT STUFF(CAST((  "
        "SELECT ', [' + COL_NAME(ic.[object_id], ic.column_id) + ']' +  "
        "CASE WHEN ic.is_descending_key = 1  "
        "THEN ' DESC'  "
        "ELSE ''  "
        "END  "
        "FROM sys.index_columns ic WITH(NOLOCK)  "
        "WHERE i.[object_id] = ic.[object_id]  "
        "AND i.index_id = ic.index_id  "
        "FOR XML PATH(N''), TYPE) AS NVARCHAR(MAX)), 1, 2, '')) + '))'  "
        "FROM sys.indexes i WITH(NOLOCK)  "
        "WHERE i.[object_id] = "+ str(object_id) + " "
        "AND i.is_primary_key = 1), '') + CHAR(13) + '' ;") #
        #print(sql)
        create_script=source.read_field(sql)
        if(full_table_name=='[TEST1].[dbo].[Config]'):
            print (create_script)
            print('Len',str(len(create_script)))
        return(create_script)




class dbhandler():
  
    
    def __init__(self,connection,current_job=None):
        self._current_job=current_job
        self._connection=connection
        self._database=self.database_name()

        pass
    def full_table_name(self,object_id,database=None):
        if(database):
            database_name=database
        else:
            database_name=self._database
        schema_name=self.schema_name(object_id)
        table_name=self.object_name(object_id)
        #print("database:"+database_name  + str(object_id))
        #print(database_name  +  table_name)
        full_name="[" + database_name + "]." + "[" + schema_name + "]." + "[" + table_name  + "]"
        return full_name
        
    def object_name(self,object_id):
        sql="select  name  from sys.objects where object_id=?"
        parameters=object_id
        table_name=self.read_field(sql,parameters)
        return table_name

    def schema_name(self,object_id):
        sql="select schema_name(schema_id) from sys.objects where object_id=?" # change for ObjectID
        #object_id=self.object_id(table)
        parameters=object_id
        schema_name=self.read_field(sql,parameters)
        return schema_name

    def object_id(self,table):
        sql="select ObjectID from catalog_tables where Name=?"
        #print (sql,table)
        object_id=self.read_field(sql,table)
        return object_id

    def has_identity(self,object_id):
        #object_id=self.object_id(table)
        sql="select (OBJECTPROPERTY("+ str(object_id) + ", 'TableHasIdentity'))"
        #print (sql)
        if(self.read_field(sql)==1):
            return True
        else:
            return False
        pass

    def database_name(self):
        database_name=self._connection.getinfo(pyodbc.SQL_DATABASE_NAME)
        return database_name
        pass

    def get_columnnames(self,object_id):        
        database= (self.database_name())
        parameters=[]
        #sql="SELECT STRING_AGG(concat('[',COLUMN_NAME,']'),',')  FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = ? and TABLE_CATALOG=?"
        sql="SELECT STRING_AGG(concat('[',name,']'),',')  FROM sys.columns WHERE object_id=?"
        #print (sql)
        parameters.append(object_id)
        column_names=self.read_field(sql,parameters)
        return column_names
        pass
 

    # def read_field(self,sql):
    #     #self._connection.execute
    #     value = self._connection.execute(sql).fetchval()
    #     return value
    def run(self,sql,parameters=None,type=2):
        success=False
        if(parameters):
            print('to Execute (wp) -> '+ sql)
            success=self._connection.execute(sql,parameters)
        else:
            if(type==1):
                cursor=self._connection.cursor()
                scripts=[]
                scripts = sql.split(';')
                for script in scripts:
                    print('to Execute -> '+ script)
                    if(script):
                        cursor.execute(script)
                cursor.commit()
                cursor.close()

                
            else:    
                print('to Execute (wop) -> '+ sql)
                success=self._connection.execute(sql)
       
       
        self._connection.commit()


        if(success):
            return True
        else:
            return False

        

    def read_field(self,sql,parameters=None):
        #self._connection.execute
        if(parameters==None):
            value = self._connection.execute(sql).fetchval()
        else:
            value= self._connection.execute(sql,parameters).fetchval()
        
        return value
    
    def get_list(self,sql):
        #list=self._connection.execute(sql).fetchall()
        list = [item[0] for item in self._connection.execute(sql).fetchall()]

        return list
        #self._connection

        #     cursor=db.cursor()
        # cursor.execute(sql)
        # records=cursor.fetchall
    def get_order(self):
        sql="select coalesce(max([Order]),0)Last from deploy_jobscripts where Job_id=?"
        parameters= (self._current_job)
        #print (sql,self._current_job)
        last_script=self.read_field(sql,parameters)
        order=last_script+1
        #print('order')
        return order

    def add(self,scripts,script_type):
        order=self.get_order()
        count=len(scripts)
        order_list=[]
        job_id=[]
        type=[]
        for i in range(order, order+count):
            order_list.append(i)
            job_id.append(self._current_job)
            #type.append(script_type)
        #print(order_list)
        cursor=self._connection.cursor()

        values=list(zip(script_type,order_list,job_id,scripts))
        sql='INSERT INTO deploy_jobscripts ([Type],[Order],[Job_id],[Script]) values (?,?,?,? )'
        #print(values)
        cursor.executemany(sql,values)
        self._connection.commit()
        

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

    def read_rows(self,sql,parameters=None):

        
        cursor=self._connection.cursor()
        if(parameters):
            cursor.execute(sql,parameters)
        else:
            cursor.execute(sql)

        records=cursor.fetchall
        dataset = []
        column_names = [column[0] for column in cursor.description ]

        for row in cursor:
            dataset.append(dict(zip(column_names,row)))

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


