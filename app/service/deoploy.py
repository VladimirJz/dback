


class target():
    def __init__(self,user,passwd,server):
        pass

class filesystem(target):
    def __init__(self, user, passwd, server):
        pass

class database(target):
    def __init__(self, user, passwd,server,port,instance):
        #super().__init__(user, passwd)
        pass
    


a=filesystem('app','12345')
print(target)