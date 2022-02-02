#!/usr/bin/python
#from pynotifier import Notification
from sys import setrecursionlimit
import pyodbc
import random
#from datetime import timedelta, date,datetime
from datetime import datetime, timedelta
from time import sleep
from alive_progress import alive_bar
import pandas as pd

class location():
    def __init__(self,path,user=None,passwd=None):
        pass

    @property
    def location(self):
        return self._location
    
    @location.setter
    def location(self,value):
        self._location=value

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
    def __init__(self,repo,source,target=None,location=None):
        print('initialize')
        self._job   =repo.current_job
        self._repo  =repo.get_connection() # repo es una connexión
        self._source=source.get_connection() # cambiar a targets
        if(target!=None):
            self._target=target.get_connection() # cambiar a targets
        else:
            self._dir='location'

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
        #print("clean:"+table)
        if(table):
            sql="TRUNCATE TABLE " + table + ";"
        else:
            sql=None
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
        source=dbhandler(self._source)
        constraints=source.read_rows(sql,object_id)
        return constraints
        
    def disable_contraints(self,object_id,disable=True):
        constraints=self.get_constraints(object_id)
        #print(constraints)
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
        script_types=[]
        script_phases=[]
        DDL=1
        DML=2
        CREATE=1

        repo=dbhandler(self._repo,self._job)
        schemas_script=self.create_schemas()
        scripts.append(schemas_script)
        script_types.append(DDL)
        script_phases.append(CREATE)

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
        items=len(filtered_tables)
        with alive_bar(items, bar = 'smooth', unknown='arrows_in', spinner = 'waves') as bar:   # default setting
            for table in filtered_tables:
                bar()
                object_id=table.get('ObjectID')
                name=table.get('Name')
                print("Creating object:" + name + " on target database")
                #print(object_id)
                create_script=self.create_table(object_id)
                if(create_script):
                    scripts.append(create_script)
                    script_types.append(DML)
                    script_phases.append(CREATE)
                else:
                    print('Table dont exists anymore')
                    #pass
            pass
            #print(scripts)
            repo.add(scripts,script_types,script_phases,progressbar=False)

    def relational_objects(self):
        sql=('select ct.[id],[ObjectID],[Name],[Schema],'
            '[Column],[FilterType],[LowerValue],[UpperValue],[ValuesDataType],'
            '[StepBy],[Table_id] '
            'from catalog_tables ct inner join (deploy_tablefilters tf '
            'inner join  deploy_tablefilters_Job tfj on tf.id=tfj.tablefilters_id) '
            'on ct.id=tf.Table_id '
            'where ct.Status=1 '
            'and tfj.jobs_id=1')
        DML=2
        DDL=1
        DATA=2
        RELATIONAL=3
        
        repo=dbhandler(self._repo,self._job)
        source=dbhandler(self._source)
        target=dbhandler(self._target)
    
        #con=self.repo.get_connection()
        #print(con)
        filtered_tables=repo.get_resulset(self._repo,sql)
        items=len(filtered_tables)
        #enable_constraints=[]
        with alive_bar(items, bar = 'smooth', unknown='arrows_in', spinner = 'waves') as bar:   # default setting
            for filter in filtered_tables:
                bar()
                scripts=[]
                script_types=[]
                script_phases=[]
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
                print("restoring relational objects  : " + table)
                full_table_name=source.full_table_name(object_id,target._database)   
                if(full_table_name):
                    constraints_script=self.disable_contraints(object_id,False)                    
                    if(constraints_script):
                        scripts.append(constraints_script)
                        script_types.append(DDL)
                        script_phases.append(RELATIONAL)
                    indexes_script=self.create_indexes(object_id)
                    if(indexes_script):
                        scripts.append(indexes_script)
                        script_types.append(DDL)
                        script_phases.append(RELATIONAL)
                if(scripts):
                    repo.add(scripts,script_types,script_phases,progressbar=False)
        pass
        

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
        DML=2
        DDL=1
        DATA=2
 
 
        repo=dbhandler(self._repo,self._job)
        source=dbhandler(self._source)
        target=dbhandler(self._target)
    
        #con=self.repo.get_connection()
        #print(con)
        filtered_tables=repo.get_resulset(self._repo,sql)
        items=len(filtered_tables)
        #enable_constraints=[]
        with alive_bar(items, bar = 'smooth', unknown='arrows_in', spinner = 'waves') as bar:   # default setting
            for filter in filtered_tables:
                bar()
                scripts=[]
                script_types=[]
                script_phases=[]
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
                print("get script data  from  : " + table)
                full_table_name=source.full_table_name(object_id,target._database)
                if(full_table_name):
                    constraints_script=self.disable_contraints(object_id)
                    
                    if(constraints_script):
                        scripts.append(constraints_script)
                        script_types.append(DDL)
                        script_phases.append(DATA)
                        #constraints_script=self.disable_contraints(object_id,False)
                        #enable_constraints.append(constraints_script)
                    truncate_script=self.clean_source(object_id)
                    #print (truncate_script)
                    if(truncate_script):
                        scripts.append(truncate_script)
                        script_types.append(DDL)
                        script_phases.append(DATA)
                    if(source.has_identity(object_id)):
                        enable_insert_id=self.enable_insert_identity(full_table_name,True)
                        scripts.append(enable_insert_id)
                        script_types.append(DDL)
                        script_phases.append(DATA)
                        
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
                                script_types.append(DML)
                                script_phases.append(DATA)

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
                                script_types.append(DML)
                                script_phases.append(DATA)
                                #print(sql)

                    if(FilterType==0):#No Filter
                        sql=insert_into + from_table
                        scripts.append(sql)
                        script_types.append(DML)
                        script_phases.append(DATA)

                    if(source.has_identity(object_id)):
                        disable_insert_id=self.enable_insert_identity(full_table_name,False)
                        scripts.append(disable_insert_id)   
                        script_types.append(DDL)
                        script_phases.append(DATA)
                    #print(scripts)
                if(scripts):
                    repo.add(scripts,script_types,script_phases,progressbar=False)
            #repo.add(enable_constraints,script_types,script_phases,progressbar=False)


                    
                    #print(enable_insert_id)
                    #print (column_names)
            
                
        print('done')
    
    
    def deploy_database(self):
        print('Deploy Start...')
        print('Running Scripts')
        target=dbhandler(self._target)
        repo=dbhandler(self._repo,self._job)
        source=dbhandler(self._source)
        sql=("select [Order],[Type] ,Script from deploy_jobscripts where Job_id=" + str(self._job) +
            "order by [Order] asc")
        deploy_scripts=repo.read_rows(sql)
        items=len(deploy_scripts)
        with alive_bar(items, bar = 'smooth', unknown='arrows_in', spinner = 'waves') as bar:   # default setting
            for script in deploy_scripts:
                bar()
                sql_script=script.get('Script')
                script_type=script.get('Type')
                order_script=script.get('Order')
                print("runing :"+ sql_script[:100] + "..")
                #print("<--")
                if(script_type==1):
                    if(target.run(sql_script,type=script_type)):
                        print('done..')
                    else:
                        print('===Error ! ==')
                else:
                    #rows=source.read_rows(sql_script)
                    query_sql=pd.read_sql_query(sql_script,self._source)
                    df=pd.DataFrame(query_sql)
                    filename="C:\dumps\\" 
                    filename=filename + 'File_' + str(order_script) + '_.csv'

                    df.to_csv(filename,index = False)

    def generate_data(self):
        print('Data:')
        sql=('select ct.[id],[ObjectID],[Name],[Schema],'
            '[Column],[FilterType],[LowerValue],[UpperValue],[ValuesDataType],'
            '[StepBy],[Table_id] '
            'from catalog_tables ct inner join (deploy_tablefilters tf '
            'inner join  deploy_tablefilters_Job tfj on tf.id=tfj.tablefilters_id) '
            'on ct.id=tf.Table_id '
            'where ct.Status=1 '
            'and tfj.jobs_id=2')
        DML=2
        DDL=1
        DATA=2
 
 
        repo=dbhandler(self._repo,self._job)
        source=dbhandler(self._source)
        #target=dbhandler(self._target)
    
        #con=self.repo.get_connection()
        #print(con)
        filtered_tables=repo.get_resulset(self._repo,sql)
        items=len(filtered_tables)
        #enable_constraints=[]
        with alive_bar(items, bar = 'smooth', unknown='arrows_in', spinner = 'waves') as bar:   # default setting
            for filter in filtered_tables:
                bar()
                scripts=[]
                script_types=[]
                script_phases=[]
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
                print("get script data  from  : " + table)
                full_table_name=source.full_table_name(object_id)
                if(full_table_name):
                    
        
                        
                    column_names=source.get_columnnames(object_id)
                    select="SELECT " + column_names 
                    from_table =" FROM " + source.full_table_name(object_id) + ""
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
                                where=" WHERE " + Column + ">=" + begin.strftime("'%Y-%m-%d'")+ " and " + Column + "<=" + end.strftime("'%Y-%m-%d'") + ";"
                                begin=end + timedelta(days=1)
                                sql=select + from_table + where
                                scripts.append(sql)
                                script_types.append(DML)
                                script_phases.append(DATA)

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
                                sql=select + from_table + where
                                scripts.append(sql)
                                script_types.append(DML)
                                script_phases.append(DATA)
                                #print(sql)

                    if(FilterType==0):#No Filter
                        sql=select + from_table
                        scripts.append(sql)
                        script_types.append(DML)
                        script_phases.append(DATA)

                if(scripts):
                    repo.add(scripts,script_types,script_phases,progressbar=False)
                    print (scripts)
            #repo.add(enable_constraints,script_types,script_phases,progressbar=False)


                    
                    #print(enable_insert_id)
                    #print (column_names)
            
                
        print('done')
    
        

        

    def ofuscate_scripts(self):
        print('Ofuscate tables')
        sql=('select [Name],[Schema],'
            '[Column],[FilterType],[LowerValue],[UpperValue],[ValuesDataType],'
            '[StepBy],[Table_id] '
            'from catalog_tables ct inner join (deploy_tablefilters tf '
            'inner join  deploy_tablefilters_Job tfj on tf.id=tfj.tablefilters_id) '
            'on ct.id=tf.Table_id '
            'where tfj.jobs_id=1')
        DML=2
       
        # obtener parametros
        script_types=[]
        script_phases=[]
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
            repo.add(scripts,script_types,script_phases)

      
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
      

    #create table script source : shorturl.at/gsFMZ
    def create_table(self,object_id): 
        source=dbhandler(self._source)
        target=dbhandler(self._target)
        full_table_name=source.full_table_name(object_id,target._database)
        if(full_table_name):
            sql=(" SELECT 'CREATE TABLE ' + '" + full_table_name  + "'+'(' + STUFF((   "
            "SELECT + char(13) + '    , [' + c.name + '] ' +    "
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
            #"CASE WHEN c.collation_name IS NOT NULL AND c.system_type_id = c.user_type_id   "  # 'til find a len string solution (len max 6353)
            "CASE WHEN 0=1 "
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
            "AND i.is_primary_key = 1), '')+ ');' ;") #
            #"AND i.is_primary_key = 1), '')+ '' ;") #
        #= 1), '')+ ');' ;

            sql=(
                "    SELECT 'CREATE TABLE ' + '" + full_table_name  + "' + CHAR(13) + '(' + CHAR(13) + STUFF((  "
                "        SELECT CHAR(13) + '    , [' + c.name + '] ' +   "
                "            CASE WHEN c.is_computed = 1  "
                "                THEN 'AS ' + OBJECT_DEFINITION(c.[object_id], c.column_id)  "
                "                ELSE   "
                "                    CASE WHEN c.system_type_id != c.user_type_id   "
                "                        THEN '[' + SCHEMA_NAME(tp.[schema_id]) + '].[' + tp.name + ']'   "
                "                        ELSE '[' + UPPER(tp.name) + ']'   "
                "                    END  +   "
                "                    CASE   "
                "                        WHEN tp.name IN ('varchar', 'char', 'varbinary', 'binary')  "
                "                            THEN '(' + CASE WHEN c.max_length = -1   "
                "                                            THEN 'MAX'   "
                "                                            ELSE CAST(c.max_length AS VARCHAR(5))   "
                "                                        END + ')'  "
                "                        WHEN tp.name IN ('nvarchar', 'nchar')  "
                "                            THEN '(' + CASE WHEN c.max_length = -1   "
                "                                            THEN 'MAX'   "
                "                                            ELSE CAST(c.max_length / 2 AS VARCHAR(5))   "
                "                                        END + ')'  "
                "                        WHEN tp.name IN ('datetime2', 'time2', 'datetimeoffset')   "
                "                            THEN '(' + CAST(c.scale AS VARCHAR(5)) + ')'  "
                "                        WHEN tp.name = 'decimal'  "
                "                            THEN '(' + CAST(c.[precision] AS VARCHAR(5)) + ',' + CAST(c.scale AS VARCHAR(5)) + ')'  "
                "                        ELSE ''  "
                "                    END +  "
                "                    CASE WHEN c.collation_name IS NOT NULL AND c.system_type_id = c.user_type_id   "
                "                        THEN ' COLLATE ' + c.collation_name  "
                "                        ELSE ''  "
                "                    END +  "
                "                    CASE WHEN c.is_nullable = 1   "
                "                        THEN ' NULL'  "
                "                        ELSE ' NOT NULL'  "
                "                    END +  "
                "                    CASE WHEN c.default_object_id != 0   "
                "                        THEN ' CONSTRAINT [' + OBJECT_NAME(c.default_object_id) + ']' +   "
                "                            ' DEFAULT ' + OBJECT_DEFINITION(c.default_object_id)  "
                "                        ELSE ''  "
                "                    END +   "
                "                    CASE WHEN cc.[object_id] IS NOT NULL   "
                "                        THEN ' CONSTRAINT [' + cc.name + '] CHECK ' + cc.[definition]  "
                "                        ELSE ''  "
                "                    END +  "
                "                    CASE WHEN c.is_identity = 1   "
                "                        THEN ' IDENTITY(' + CAST(IDENTITYPROPERTY(c.[object_id], 'SeedValue') AS VARCHAR(5)) + ',' +   "
                "                                        CAST(IDENTITYPROPERTY(c.[object_id], 'IncrementValue') AS VARCHAR(5)) + ')'   "
                "                        ELSE ''   "
                "                    END   "
                "            END  "
                "        FROM sys.columns c WITH(NOLOCK)  "
                "        JOIN sys.types tp WITH(NOLOCK) ON c.user_type_id = tp.user_type_id  "
                "        LEFT JOIN sys.check_constraints cc WITH(NOLOCK)   "
                "            ON c.[object_id] = cc.parent_object_id   "
                "            AND cc.parent_column_id = c.column_id  "
                "        WHERE c.[object_id] =  "+ str(object_id) +"  "
                "        ORDER BY c.column_id  "
                "        FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 7, '      ') +   "
                "        ISNULL((SELECT '  "
                "        , CONSTRAINT [' + i.name + '] PRIMARY KEY ' +   "
                "        CASE WHEN i.index_id = 1   "
                "            THEN 'CLUSTERED'   "
                "            ELSE 'NONCLUSTERED'   "
                "        END +' (' + (  "
                "        SELECT STUFF(CAST((  "
                "            SELECT ', [' + COL_NAME(ic.[object_id], ic.column_id) + ']' +  "
                "                    CASE WHEN ic.is_descending_key = 1  "
                "                        THEN ' DESC'  "
                "                        ELSE ''  "
                "                    END  "
                "            FROM sys.index_columns ic WITH(NOLOCK)  "
                "            WHERE i.[object_id] = ic.[object_id]  "
                "                AND i.index_id = ic.index_id  "
                "            FOR XML PATH(N''), TYPE) AS NVARCHAR(MAX)), 1, 2, '')) + ')'  "
                "        FROM sys.indexes i WITH(NOLOCK)  "
                "        WHERE i.[object_id] = "+ str(object_id) + "  "
                "            AND i.is_primary_key = 1), '') + CHAR(13) + ');'  "
                )
        if(full_table_name=='[TEST1].[dbo].[Config]'):
           print(sql)

        if(full_table_name):
            create_script=source.read_field(sql)
            create_script=create_script.replace("     ,",",")
        
            if(full_table_name=='[TEST1].[dbo].[Config]'):
                print (create_script)
                print('Len:',str(len(create_script)))
        else:
            create_script=None
        return(create_script)

    #create index source(thanks): shorturl.at/ioEHZ
    def create_indexes(self,object_id):
        source=dbhandler(self._source)
        target=dbhandler(self._target)
        scripts=[]
        full_table_name=source.full_table_name(object_id,target._database)
        if(full_table_name):
            sql= ("SELECT  CASE si.index_id WHEN 0 THEN N'' "
                "    ELSE  "
                "        CASE is_primary_key WHEN 1 THEN  "
                "            N'ALTER TABLE ' + '"   + full_table_name +  " ' +N' ADD CONSTRAINT ' + QUOTENAME(si.name) + N' PRIMARY KEY ' +  "
                "                CASE WHEN si.index_id > 1 THEN N'NON' ELSE N'' END + N'CLUSTERED '  "
                "            ELSE N'CREATE ' +  "
                "                CASE WHEN si.is_unique = 1 then N'UNIQUE ' ELSE N'' END + "
                "                CASE WHEN si.index_id > 1 THEN N'NON' ELSE N'' END + N'CLUSTERED ' + "
                "                N'INDEX ' + QUOTENAME(si.name) + N' ON ' +'" + full_table_name + " '"
                "        END + "
                "        /* key def */ N'(' + key_definition + N')' + "
                "        /* includes */ CASE WHEN include_definition IS NOT NULL THEN  "
                "            N' INCLUDE (' + include_definition + N')' "
                "            ELSE N'' "
                "        END + "
                "        /* filters */ CASE WHEN filter_definition IS NOT NULL THEN  "
                "            N' WHERE ' + filter_definition ELSE N'' "
                "        END + "
                "        CASE WHEN row_compression_partition_list IS NOT NULL OR page_compression_partition_list IS NOT NULL  "
                "            THEN N' WITH (' + "
                "                CASE WHEN row_compression_partition_list IS NOT NULL THEN "
                "                    N'DATA_COMPRESSION = ROW ' + CASE WHEN psc.name IS NULL THEN N'' ELSE + N' ON PARTITIONS (' + row_compression_partition_list + N')' END "
                "                ELSE N'' END + "
                "                CASE WHEN row_compression_partition_list IS NOT NULL AND page_compression_partition_list IS NOT NULL THEN N', ' ELSE N'' END + "
                "                CASE WHEN page_compression_partition_list IS NOT NULL THEN "
                "                    N'DATA_COMPRESSION = PAGE ' + CASE WHEN psc.name IS NULL THEN N'' ELSE + N' ON PARTITIONS (' + page_compression_partition_list + N')' END "
                "                ELSE N'' END "
                "            + N')' "
                "            ELSE N'' "
                "        END + "
                "        ' ON [PRIMARY] '  "
                #"		-- + CASE WHEN psc.name is null THEN ISNULL(QUOTENAME(fg.name),N'') ELSE psc.name + N' (' + partitioning_column.column_name + N')' END "
                "        + N';' "
                "    END AS script "
                "     "
                "FROM sys.indexes AS si "
                "JOIN sys.tables AS t ON si.object_id=t.object_id "
                "JOIN sys.schemas AS sc ON t.schema_id=sc.schema_id "
                "LEFT JOIN sys.dm_db_index_usage_stats AS stat ON  "
                "    stat.database_id = DB_ID()  "
                "    and si.object_id=stat.object_id  "
                "    and si.index_id=stat.index_id "
                "LEFT JOIN sys.partition_schemes AS psc ON si.data_space_id=psc.data_space_id "
                "LEFT JOIN sys.partition_functions AS pf ON psc.function_id=pf.function_id "
                "LEFT JOIN sys.filegroups AS fg ON si.data_space_id=fg.data_space_id "
                "/* Key list */ OUTER APPLY ( SELECT STUFF ( "
                "    (SELECT N', ' + QUOTENAME(c.name) + "
                "        CASE ic.is_descending_key WHEN 1 then N' DESC' ELSE N'' END "
                "    FROM sys.index_columns AS ic  "
                "    JOIN sys.columns AS c ON  "
                "        ic.column_id=c.column_id   "
                "        and ic.object_id=c.object_id "
                "    WHERE ic.object_id = si.object_id "
                "        and ic.index_id=si.index_id "
                "        and ic.key_ordinal > 0 "
                "    ORDER BY ic.key_ordinal FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'),1,2,'')) AS keys ( key_definition ) "
                "/* Partitioning Ordinal */ OUTER APPLY ( "
                "    SELECT MAX(QUOTENAME(c.name)) AS column_name "
                "    FROM sys.index_columns AS ic  "
                "    JOIN sys.columns AS c ON  "
                "        ic.column_id=c.column_id   "
                "        and ic.object_id=c.object_id "
                "    WHERE ic.object_id = si.object_id "
                "        and ic.index_id=si.index_id "
                "        and ic.partition_ordinal = 1) AS partitioning_column "
                "/* Include list */ OUTER APPLY ( SELECT STUFF ( "
                "    (SELECT N', ' + QUOTENAME(c.name) "
                "    FROM sys.index_columns AS ic  "
                "    JOIN sys.columns AS c ON  "
                "        ic.column_id=c.column_id   "
                "        and ic.object_id=c.object_id "
                "    WHERE ic.object_id = si.object_id "
                "        and ic.index_id=si.index_id "
                "        and ic.is_included_column = 1 "
                "    ORDER BY c.name FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'),1,2,'')) AS includes ( include_definition ) "
                "/* Partitions */ OUTER APPLY (  "
                "    SELECT  "
                "        COUNT(*) AS partition_count, "
                "        CAST(SUM(ps.in_row_reserved_page_count)*8./1024./1024. AS NUMERIC(32,1)) AS reserved_in_row_GB, "
                "        CAST(SUM(ps.lob_reserved_page_count)*8./1024./1024. AS NUMERIC(32,1)) AS reserved_LOB_GB, "
                "        SUM(ps.row_count) AS row_count "
                "    FROM sys.partitions AS p "
                "    JOIN sys.dm_db_partition_stats AS ps ON "
                "        p.partition_id=ps.partition_id "
                "    WHERE p.object_id = si.object_id "
                "        and p.index_id=si.index_id "
                "    ) AS partition_sums "
                "/* row compression list by partition */ OUTER APPLY ( SELECT STUFF ( "
                "    (SELECT N', ' + CAST(p.partition_number AS VARCHAR(32)) "
                "    FROM sys.partitions AS p "
                "    WHERE p.object_id = si.object_id "
                "        and p.index_id=si.index_id "
                "        and p.data_compression = 1 "
                "    ORDER BY p.partition_number FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'),1,2,'')) AS row_compression_clause ( row_compression_partition_list ) "
                "/* data compression list by partition */ OUTER APPLY ( SELECT STUFF ( "
                "    (SELECT N', ' + CAST(p.partition_number AS VARCHAR(32)) "
                "    FROM sys.partitions AS p "
                "    WHERE p.object_id = si.object_id "
                "        and p.index_id=si.index_id "
                "        and p.data_compression = 2 "
                "    ORDER BY p.partition_number FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'),1,2,'')) AS page_compression_clause ( page_compression_partition_list ) "
                "WHERE  "
                "    si.type IN (0,1,2) /* heap, clustered, nonclustered */ "
                "	AND t.object_id= " + str(object_id) + " "
                "ORDER BY  si.index_id "
                "    OPTION (RECOMPILE); ")
            print(sql)
            index_scripts=source.read_rows(sql)
            for index in index_scripts:
                script=index.get('script')
                scripts.append(script)
            sql = ' '.join([str(sentence) for sentence in scripts])
        return sql
        


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
        if(table_name,schema_name,database):
            try:
                full_name="[" + database_name + "]." + "[" + schema_name + "]." + "[" + table_name  + "]"
            except:
                full_name=None
        else:
            full_name=None
        return full_name
        
    def object_name(self,object_id):
        sql="select  name  from sys.objects where object_id=?"
        parameters=object_id
        try:
            table_name=self.read_field(sql,parameters)
        except:
            print('The object_id dont exists')
            table_name=None
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
            #print('to Execute (wp) -> '+ sql)

            success=self._connection.execute(sql,parameters)
        else:
            if(type==1):
                cursor=self._connection.cursor()
                scripts=[]
                scripts = sql.split(';')
                for script in scripts:
                    #print('to Execute -> '+ script)
                    if(script):
                        cursor.execute(script)
                cursor.commit()
                cursor.close()

                
            else:    
                #print('to Execute (wop) -> '+ sql)
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

    def add(self,scripts,script_type,script_phases,progressbar=False):
        if (progressbar):
            with alive_bar( bar = 'smooth', unknown='arrows_in', spinner = 'waves') as bar:  
                self.insert(scripts,script_type,script_phases)
                bar()
        else:
            self.insert(scripts,script_type,script_phases)
        


    def insert(self,scripts,script_type,script_phase):
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

        values=list(zip(script_type,order_list,job_id,scripts,script_phase))
        #print(scripts)
        sql='INSERT INTO deploy_jobscripts ([Type],[Order],[Job_id],[Script],[Phase]) values (?,?,?,?,?)'
        #print(values)
        
        cursor.executemany(sql,values)
        self._connection.commit()
        

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


