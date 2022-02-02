

jobs[]
    deploy[]
    dump[]
        core[]
            index
            keys
            entity

            database[]
                connection:
                exec
                run

                msql[]
_props  
target
    database[]
    filesystem[]
source
    database[]



78088419425

target=objects.location('172.16.20.3',1414,'sa','#1Qazse4',database='DESARROLLO',engine='mssql')

print(target.server)
print(target.user)
target.user='usuario'
print(target.user)
print(target.port)
print(target.passwd)
print(target.database)
target.database='DESARROLLO2'
print(target.database)

repo=objects.repository('172.16.20.3',1414,'sa','#1Qazse4',database='dba',engine='msql',loginuser='vjimenezv')
print(repo.server)
print(repo.user)
repo.user='app'
print(repo.user)
print(repo.port)
print(repo.passwd)
print(repo.database)
repo.database='DBA'
print(repo.database)
print(repo.loginuser)
repo.loginuser='vjime'
print(repo.loginuser)
print(target.driver)
target.get_stringconnection()
repo.get_stringconnection()
