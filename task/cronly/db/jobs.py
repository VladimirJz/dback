#django
import os
import sys
import django
from django.db.models import Value
from django.db.models import Count, F, Value

sys.dont_write_bytecode = True
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

# own
from db.models import *
from datetime import datetime, timedelta
from dateutil import parser
import shutil
import subprocess

from ctypes import sizeof
from inspect import Parameter
from db.models import Backups, Credentials, DataBases, Jobs,JobSchedule
import time
from  datetime import datetime
import shutil,os
import subprocess


class rotation():
    def run(self):
        PATH_7Z='C:\\Util\\7za.exe'
        ZIP_OPTIONS=' a -t7z '


        current_date=datetime.now()
        print (current_date)

        IEEPO_backups=Backups.objects.all().filter(Job_id=1)

        #backups=Backups.objects.all().values('id','FileName','Job__JobName','CreationDate','Job__his_rules')
        #PRUEBAS con IEEPO DB
        enabled_jobs=Jobs.objects.all().filter(id=1)
        print('Jobs activos: ', enabled_jobs)
        print('Evaluando')
        print('')
        for job in enabled_jobs:
            
            #rules=RotationRules.objects.all().filter(Job_id=job.id).order_by('Order').only('id','RuleName','RetentionDays','FileTag','ZipFile','ZipFormat','Location_id','Location__AbsolutePath','Location__LocationName')
            rules=RotationRules.objects.all().filter(Job_id=job.id).order_by('Order').only('id','RuleName','RetentionDays','FileTag','ZipFile','ZipFormat','Location_id').select_related('Location')
            current_job_id=job.id
            backups=Backups.objects.all().filter(Job_id=current_job_id,Status__lt=5).select_related('Location').order_by('-CreationDate')
            backups_count=backups.count()
            print('No de backups encontrados:',backups_count)
            for current_backup in backups:
                days_old=current_backup.days_old()
                backup_location_id=current_backup.Location_id
                current_backup_id=current_backup.Location_id
                file_name= current_backup.FileName
                new_filename=file_name
                current_comments=current_backup.Comments
                comments=current_comments
                current_location_path=current_backup.Location.AbsolutePath
                current_rule=rules.filter(RetentionDays__gte=days_old,Location_id=backup_location_id)
                print('')
                print(':::::::::::::::::::::::::::::::::')
                print('Backup:' ,file_name)
                print('_________________________________')
                print('Fecha Crecion: ', current_backup.CreationDate)
                print('Dias antigüedad.: ', days_old ,' , Localizado en :', current_backup.Location.LocationName, ' - ', current_location_path)
                

                #si el backup esta en la regla correcta.
                if(current_rule):
                    print('Regla: ',current_rule)
                    print('La ubicación actual es correcta')
                    print ('[>>] Backup resguardado correctamente.')
                    print(' ')
                else:
                    next_rule=rules.filter(RetentionDays__gte=days_old).order_by('Order')[:1]
                    if(next_rule):
                        print ('Transferir >')
                        print ('Sigiente Regla: ',next_rule)
                        print('Location id: ',backup_location_id)
                        print(" ")

                        for  rule in next_rule:
                            print('Regla aplicable:', rule)
                            next_location_id=rule.Location_id
                            next_location_name=rule.Location.LocationName
                            next_location_path=rule.Location.AbsolutePath
                            print('Transferir a: ', next_location_name, ': ', next_location_path)
                            if(rule.ZipFile):
                                next_zip_format=rule.get_ZipFormat_display()
                            else:
                                next_zip_format=None
                                print('Formato a aplicar : ', next_zip_format,'')
                            comments=current_backup.Comments
                            #comments=comments + '_nuevo'

                            current_filename=current_location_path +  '\\' + current_backup.FileName
                            next_filename=next_location_path + '\\' + current_backup.FileName

                            print (current_filename)
                            print (next_zip_format,'>>', next_filename)
                            print('')
                            print('     Buscando archivo.')
                            if os.path.isfile(current_filename):
                                print('[>>] Backup localizado')
                                
                                print('     Transferir a ubicación destino')
                                print('     ', current_location_path,' >> ',next_location_path)
                                print('     copiando...')
                                shutil.copy(current_filename,next_filename)
                                if(os.path.isfile(next_filename)):
                                    print('[>>] Copia Exitosa')
                                    if(next_zip_format):
                                        new_filename+= next_zip_format
                                        next_zip_filename= next_filename + next_zip_format
                                        zip_command=PATH_7Z + ZIP_OPTIONS + next_zip_filename + next_filename
                                        print('     Comprimiento...')
                                        subprocess.call(zip_command)
                                        if(os.path.isfile(next_zip_filename)):
                                            print('[>>] Compresión terminada')
                                            if(os.path.isfile(next_filename)):
                                                print('     Removimendo copia sin comprimir')
                                                os.remove(next_filename)
                                                print('[>>] Copia eliminada')
                                        else:
                                            print('[--] Ocurrio un error al comprimir el archivo')
                                            comments+= '. Ocurrio un error al transferir el backup.'
                                            backups_status=3
                            
                                print('[>>] Backups transferido correctamente.')
                                if(os.path.isfile(current_filename)):
                                    print('     Removiendo backups de la ubicación original')
                                    os.remove(current_filename)
                                    print('[>>] Copia original eliminada')
                                    backups_status=1
                                
                                else:
                                    print('[--] Error al copiar el backup')
                                    comments+= '. Ocurrio un al leer el archivo, podria estar dañado.'

                                    backups_status=4
                            else:
                                print('[--] Error backup no localizado')
                                comments+= '. El archivo no se encuentra en la ruta descrita.'
                                backups_status=3
                                
                            #actualizad backup
                            Backups.objects.filter(id=current_backup_id).update(Status=backups_status,Location=next_location_id,Comments=comments, FileName=new_filename )
                            print('[>>] Regla procesada.')
                            print(' ')

                    else:
                        print('     No existe una regla activa el archivo')
                        print('     el backup caducó')
                        backup_status=5
                        comments= 'Caducó la vigencia del backup, el archivo fue eliminado'
                        if os.path.isfile(current_filename):
                            print('[>>] Eliminando backup vencido')
                            os.remove(current_filename)
                            if os.path.isfile(current_filename):
                                print('[--] Error, no se pudo eliminar el backup caducado.')
                                comments='Error al eliminar el backup caducado.'
                                backups_status=4
                        else:
                            print('     El archivo fue removido previamente.')
                            comments='El archivo fue removido.'
                            backups_status=5
                        Backups.objects.filter(id=current_backup_id).update(Status=backups_status,Comments=comments )
                    print(':::::::::::::::::::::::::::::::::')
                    print(' ')
                    print(' ')
                            
class backup():
    def run(self):   
        # Backups utilities
        # TODO: find the way to locate binaries
        MYSQLDUMP_PATH='C:\Program Files\MariaDB 10.6\\bin'
        MARIADB_MYSQLDUMP_PATH="""C:\\Program Files\\MariaDB 10.6\\bin"""
        MYSQLDUMP='mysqldump.exe'
        PGADMIN_PGDUMP_PATH="""C:\\Program Files\\pgAdmin 4\\v6\\runtime"""
        PGDUMP="pg_dump.exe"
        
        #
        SUCCESS_MESSAGE='Backup generado correctamente.'
        ERROR_STATUS  = 2
        SUCCESS_STATUS =1
        ERROR_MESSAGE=""
        #status
        AVAILABLE=1
        DONTEXISTS=2
        



        backup_date = time.strftime('%Y%m%d')
        current_date=time.strftime('%Y-%m-%d')
        current_datetime=datetime.now()
        size=0
        size_mb=0 

        print('')
        print(">> Ejecutando Jobs de respaldo.")
        schedules=JobSchedule.objects.all().select_related('Job')
        #schedules=JobSchedule.objects.filter(UseRemotePath==True).select_related('Job')
       # schedules=JobSchedule.objects.filter(Schedule=2)
        print('   Jobs activos:',schedules.count())
        for  schedule in schedules:
            print('')
            print(':::::::::::::::::::::::::::::::::')
            job=schedule.Job
            type=str(schedule.get_Schedule_display())
            is_local=(schedule.Job.IsLocal)
            network_save=(schedule.Job.UseRemotePath)
            use_bypass_dir=(schedule.Job.UseByPassDir)
            bypass_dir=(schedule.Job.ByPassDir)
            absolute_path=(schedule.Job.Location.AbsolutePath)
            remote_path=schedule.Job.Location.RemotePath
            location=schedule.Job.Location
            print(remote_path)
            database_name=schedule.Job.Database.Database
            database_id=schedule.Job.Database.id
            print("Running job [" + type + "], for database " + database_name)
            database=DataBases.objects.only('Server__id','Server__Host','Server__Type','Server__Port').get(id=database_id)
            server_host=database.Server.Host
            server_type=database.Server.get_Type_display()
            server_type_id=database.Server.Type
            server_port=database.Server.Port
            
            print("[>>] Server:", server_host," (", server_type,")")
            backup_file_name=database_name

            credentials=Credentials.objects.get(Server_id=database.Server_id)
            user=credentials.User
            passw=credentials.Pass
            params=[]

            
          

            if server_type_id==2 :
                precommand=''
                path=MARIADB_MYSQLDUMP_PATH
                exe=MYSQLDUMP
                login_params='-u ' + user + ' -p' + passw
                host_params='-h ' + server_host + ' -P' + str(server_port)
                database_params=database_name
                
                
            if server_type_id==3 :
                path=PGADMIN_PGDUMP_PATH
                exe=PGDUMP
                precommand='set PGPASSWORD=' + passw + '&&'
                login_params='-U ' + user  
                host_params='-h ' + server_host
                database_params='-d ' + database_name

            
            path_exe=path +'\\'+ exe
            print("[>>] Utilieria :", exe)
            
            target='>'
            if(network_save):
                backup_path=remote_path
            else:
                backup_path=absolute_path
                

            
            print("[>>] Registrando backup.")
            backup_file_name=database_name +'_' +  backup_date + '.sql'
            full_backup_name=backup_path + '\\' + backup_file_name
            backup=Backups.objects.create(Job=job,
                                        Database=database,
                                        Status_id=AVAILABLE,
                                        Location=location,
                                        CreationDate=datetime.today(),
                                        StartBackup=datetime.now(),
                                        FileName=backup_file_name)


            backup.save()
            if(os.path.exists(path_exe)):   
                
                path_exe='"' + path_exe + '"'
                params.append(precommand)
                params.append(path_exe)
                params.append(login_params)
                params.append(host_params)
                params.append(database_params)
                params.append('>')
                params.append(full_backup_name)
                #print(user,passw)
                #print (params)
                backup_command=' '.join(params)
                print(backup_command)
                print("[>>] Ejecutando Job.")
                print("     " + path_exe)
                #subprocess.call([path_exe,],shell=True)
                #subprocess.call([path_exe,"-u","remote","-p12345","-h","10.186.1.154","--compact","test_b"," > "+r"C:\respaldo\recursos_materiales_20220304_2.sql" ])
                print (backup_command)

                os.system(backup_command)
                    
                    # look for the file.

                if(os.path.exists(full_backup_name)):
                    print("[>>] Backup generado.")
                    size=os.path.getsize(full_backup_name)
                    if(size>0):
                        size_mb=size/1024/1000
                    else:
                        print("[--] El archivo esta dañado, " + backup_file_name)
                        ERROR_MESSAGE='Error: El archivo esta vacio ' + backup_file_name
                else:
                    if(os.path.exists(backup_path)):
                        print("[--] El archivo no existe, ", backup_file_name)
                        ERROR_MESSAGE='Error :El backup no fue generado ' + backup_file_name
                    else:
                        print("[--] No se tiene acceso a la ubicación: " + backup_path )
                        ERROR_MESSAGE='Error :El directorio destino no esta disponible ' + backup_path


                if(ERROR_MESSAGE):
                    MESSAGE=ERROR_MESSAGE
                    STATUS=ERROR_STATUS
                    size=0
                    size_mb=0
                    print("[--] Error al generar el backup, " + backup_file_name)
                    
                else:
                    MESSAGE=SUCCESS_MESSAGE
                    STATUS=SUCCESS_STATUS
                    print("[>>] Backup generado correctamente,  " + backup_file_name)
                
            else:
                ERROR_MESSAGE="Error: No se encontro la utileria " + exe
                MESSAGE=ERROR_MESSAGE
                STATUS=ERROR_STATUS
                print("[--] Error: No se encontro la utileria " + exe)
                print 
                print("[--] Error al generar el backup, " + backup_file_name)
            
            Backups.objects.filter(id=backup.id).update(Status_id=STATUS,
                                                        Size=size,
                                                        SizeMB=size_mb,
                                                        EndBackup=datetime.now(),
                                                        Updated=datetime.now(),
                                                        Comments=MESSAGE)


            print("[>>] Bitacora actualizada, " + backup_file_name)



   


