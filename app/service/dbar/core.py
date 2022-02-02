from multiprocessing import ProcessError
from django.db import connection
from numpy import source
import pyodbc
import pandas
from  utils import objects
from database import dbhandler as db
class database():
    def __init__(self,location):
        self._stringconnection=location.get_stringconnection()
        print(location.get_stringconnection())
        pass
    def connection(self):
        db_connection=pyodbc.connect(self._stringconnection)  
        print('Success Connection to ' + self._database )       
        return db_connection
        


class workspace(): 
    class job():
        def __init__(self,repository_location,source_location,target_location):
            self._repository_strcon=(repository_location.get_stringconnection())
            self._source_strcon=(source_location.get_stringconnection())
            self._target_strcon=(target_location.get_stringconnection())
            #self.job_id=0
            self.outer_var = 1
            pass 
        @property
        def job_id(self):
            return self._job_id
            
        @job_id.setter
        def job_id(self,value):
            self._job_id=value
        
        
        def source(self):
            return self._source(self)
        
        def target(self):
            return self._target(self)
        
        def repository(self):
            return self._repository(self)
        
        # def set_job(self,job_id):
        #     self.job_id=job_id
        #     pass

        def get_inner_object(self):
            return self.connection(self)
            print('get inner')
    
        class connection():
            def __init__(self,job):
                self.job = job
                #self.get_connection()
               # print('var:',self.outer.outer_var)

                pass
            def get_connection(self):
                db_strcon= self.stringcon()
                db_connection=pyodbc.connect(db_strcon)  
                print('Success Connection to',db_connection.getinfo(pyodbc.SQL_DATABASE_NAME))       
                return db_connection

            def inner_var(self):
                return self.job.outer_var      
            

            @property
            def stringconnection(self):
                return self._stringconnection
            
            @stringconnection.setter
            def stringconnection(self,value):
                self._stringconnection=value

            def imprime(self):
                print('imprimiendo')
            

            def clean(self):
                db=self.get_connection()
                print(db)
                print('Cleaned')
                pass      

        class _source(connection):
            def __init__(self,job):
                super().__init__(job)
                #print(self._source_location)
            def stringcon(self):
                return self.job._source_strcon   
                
                
                pass

        class _target(connection):
            def __init__(self,job):
                super().__init__(job)
            
            def stringcon(self):
                return self.job._target_strcon   
                
                

        class _repository(connection):
            def __init__(self,job):
                super().__init__(job)
             
            def stringcon(self):
                return self.job._repository_strcon   

    
    class deploy(job):
        def __init__(self,repository,source,target):
            super().__init__(repository,source,target)
            pass
        def clean(self):
            print('cleaned deploy repository')
            #print(self.repository().stringcon())
            repodb=self.repository().get_connection()
            sourcedb=self.source().get_connection()
            targetdb=self.target().get_connection()
            # con=r.get_connection()
            # repo=db(con)
            # print(repo)
            # print(repo.database_name())
            repository=db(repodb)
            repository.object_id('')

            pass
    
    class dumpdata(job):
            pass




sourcel=objects.location('172.16.20.3',1414,'sa','#1Qazse4',database='IEEPODIC',engine='mssql')
targetl=objects.location('172.16.20.3',1414,'sa','#1Qazse4',database='DESARROLLO',engine='mssql')
repol=objects.repository('172.16.20.3',1414,'sa','#1Qazse4',database='dba',engine='mssql',loginuser='vjimenezv')

deploy = workspace.deploy(repol,targetl,sourcel)
deploy.job_id=1 #set job_id
deploy.clean()


print("---")

#source=deploy.source()
#target=deploy.target()
#repo=deploy.repository()
print("---")

#print(source.stringcon())
#print(target.stringcon())
#print(repo.stringcon())

#source.get_connection()



#transfer=workspace.deploy(repol,targetl,sourcel)

#print(type(transfer)) # '__main__.workspace.deploy'
#print(transfer.source) #'__main__.workspace.job.source


# print(transfer.source.stringconnection)
# print(transfer.target.stringconnection)
# print(transfer.repository.stringconnection)







