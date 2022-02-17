#!/usr/bin/python

import pyodbc
import os
import pipes
import time
from  datetime import datetime
job_id=2
DB_USER ='root'
DB_USERPASSW ='#1Qazse4#'
DB_HOST='localhost'
SUCCESS_MESSAGE='Backup generado correctamente.'
ERROR_STATUS  = 2
SUCCESS_STATUS =1

#TODO: se debe iterar sobre Servidor_id para generar el backup de todas sus bases de datos
#       quitar las credenciales del script!


ERROR_MESSAGE=''

host_ip='db.ieepo.gob.mx'
string_connection=("Driver={ODBC Driver 17 for SQL Server};"
                    "Server=db.ieepo.gob.mx\\MSSQLServer2,1414;"
                    "Database=dba;"
                    "UID=monitor;"
                    "PWD=#1Qazse4#;")

db=pyodbc.connect(string_connection)

backup_date = time.strftime('%Y%m%d')
current_date=time.strftime('%Y-%m-%d')
current_datetime=datetime.now() 

print (current_datetime)
print (current_date)
sql=(" select [Database],bj.Database_id ,bj.Location_id ,bj.ByPassDir,bj.UseByPassDir,RemotePath "
     " from catalog_databases cd inner join  ( backup_jobs bj  inner join backup_locations bl  on bj.Location_id =bl.id) "
     " on cd.id=bj.Database_id  "
     " where bj.id=?"
     )

cursor=db.cursor()
cursor.execute(sql,job_id)
rows = cursor.fetchall()
for row in rows:
    location_id=int(row.Location_id)
    database_name=row.Database
    database_id=int(row.Database_id)
    use_bypass_dir=row.UseByPassDir
    by_pass_dir=row.ByPassDir
    remote_path=row.RemotePath
    backup_file_name=database_name +'_' +  backup_date + '.sql'
    if(use_bypass_dir):
        destination_path=by_pass_dir 
    else:
        destination_path=RemotePath 
    
    
    fullpath_backup=destination_path + '/' + backup_file_name


    current_datetime=datetime.now() 
    parameters=[]

    new_backup=("INSERT INTO dba.[dbo].[backup_files] "
                " ([Database_id],[Job_id],[CreationDate],[StartBackup],[FileName],[Location_id]) "
                " VALUES (?,?,?,?,?,?);")
    parameters=[database_id,job_id,current_date,current_datetime,backup_file_name,location_id]
    
    
    print(type(job_id))
    print(type(database_id))
    print(type(location_id))



    print(new_backup)
    cursor.execute(new_backup,parameters)
    cursor.execute("SELECT @@IDENTITY AS ID;")
    backup_id=cursor.fetchone()[0]
    print (backup_id)
    cursor.commit()
    #run backup
    backup_command= "mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USERPASSW + " " + database_name + " > " + pipes.quote(fullpath_backup)
    print(backup_command)
    #os.system(backup_command)
    print('Done')
    
    # look for the file.

    if(os.path.exists(fullpath_backup)):
        size=os.path.getsize(fullpath_backup)
        if(size>0):
            size_mb=size/1024/1000
            print(size,size_mb)
        else:
            ERROR_MESSAGE='Error: El archivo esta vacio ' + backup_file_name
    else:
        if(os.path.exists(destination_path)):
            ERROR_MESSAGE='Error :El backup no fue generado ' + backup_file_name
        else:
            ERROR_MESSAGE='Error :El directorio destino no esta disponible ' + destination_path


    if(ERROR_MESSAGE):
        MESSAGE=ERROR_MESSAGE
        STATUS=ERROR_STATUS
        size=0
        size_mb=0
        
    else:
        MESSAGE=SUCCESS_MESSAGE
        STATUS=SUCCESS_STATUS

                
                       
    update_backup=("UPDATE dba.dbo.backup_files "
                       "SET Status_id=?, "
                       "    Comments=?, "
                       "    EndBackup=?, "
                       "    Size=? , "
                       "    SizeMB=? "
                       "WHERE id=?"
                       )
    parameters=[STATUS,MESSAGE,current_datetime,size,size_mb,backup_id]
    cursor.execute(update_backup,parameters)
    cursor.commit()
cursor.close()
db.close()

    





    





























