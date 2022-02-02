class objects():    
    class location():
        '''Define a working location (DB/Filesystem)'''
        def __init__(self,server,port,user,passwd,database=None,instance=None,engine=None,dir=None):
            self.server=server
            self.port=port
            self.user=user
            self.passwd=passwd
            self.database=database
            self.instance=instance
            self.engine=engine
            self.dir=dir
            self.driver=self.get_driver()
           
            pass
    
        def get_driver(self):
            if(self.engine=='mssql'):
                return 'ODBC Driver 17 for SQL Server'


        @property
        def server(self):
            return self._server       
        @server.setter
        def server(self,value):
            self._server = value
        
        @property
        def port(self):
            return self._port       
        @port.setter
        def port(self,value):
            self._port = value

        @property
        def user(self):
            return self._user
        @user.setter
        def user(self,value):
            self._user = value

        @property
        def passwd(self):
            return self._passwd  
        
        @passwd.setter
        def passwd(self,value):
            self._passwd = value
        
        @property
        def database(self):
            return self._database 
        
        @database.setter
        def database(self,value):
            self._database = value

        @property
        def instance(self):
            return self._instance 
        
        @instance.setter
        def instance(self,value):
            self._instance = value

        @property
        def engine(self):
            return self._engine 
        
        @engine.setter
        def engine(self,value):
            self._engine = value


        @property
        def driver(self):
            return self._driver    

        @driver.setter
        def driver(self,value):
            self._driver = value
        

        
        def get_stringconnection(self):
            db_constring=("Driver="+ self._driver + ";"
                    "Server="+  self._server +";"
                    "Database="+ self._database + ";"
                    "UID=" + self._user + ";"
                    "PWD="+ self._passwd +";")
            return db_constring
        

    class repository(location):
        '''Define the job repository (DB)'''
        def __init__(self,server,port,user,passwd,database=None,instance=None,engine=None,dir=None,loginuser=None,loginpasswd=None):
            super().__init__(server,port,user,passwd,database=database,instance=instance,engine=engine,dir=dir)
            self.loginuser=loginuser
            self.loginpasswd=loginpasswd
            #self.driver=self.get_driver()

                    
        @property
        def loginuser(self):
            return self._loginuser 
        
        @loginuser.setter
        def loginuser(self,value):
            self._loginuser = value


        @property
        def loginpasswd(self):
            return self._loginpasswd 
        
        @loginpasswd.setter
        def loginpasswd(self,value):
            self._loginpasswd = value        