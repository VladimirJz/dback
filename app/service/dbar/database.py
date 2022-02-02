import pyodbc
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
     