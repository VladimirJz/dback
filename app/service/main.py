#!/usr/bin/python
#db configuration
from ast import dump
from database import connection, transfer_job,location
from types import SimpleNamespace    
from database import admin_connection

#server=connection('172.16.20.3','sa','#1Qazse4')
source=connection('172.16.20.3','sa','#1Qazse4')
source.database='IEEPODIC'

target=connection('172.16.20.3','sa','#1Qazse4')
target.database='TEST4'

dir=location('/home/vladimir/Documents/IE/')

repo=admin_connection('172.16.20.3','sa','#1Qazse4',2)


#repo.get_connection()
#syncdb=transfer_job(repo,source,target)
#syncdb.initialize()
#syncdb.create_target_database()
#syncdb.generate_data_scripts()
#syncdb.relational_objects()
#syncdb.deploy_database()
#syncdb.ofuscate_scripts()
#repo.get_connection()
dumpdata=transfer_job(repo,source=source,target=target,location=dir)
dumpdata.initialize()
dumpdata.generate_data()
dumpdata.deploy_database()





# server.database='IEEPO'
# source=server.get_connection()
# server.database='DESARROLLO'
# target=server.get_connection()
# server.database='dba'
# repo=server.get_connection()

#syncdb=transfer_job(server,'IEEPO',1)





