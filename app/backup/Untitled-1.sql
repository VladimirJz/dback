
-- ------------------------------
--  JOB DE GENERACION DE BACKUPS
--  STEP : 1 
-- ------------------------------


DECLARE @Var_Archivo VARCHAR(255)
DECLARE @Var_Fecha VARCHAR(255)
DECLARE @Var_TableRows   varchar(max)
DECLARE @Var_TableHeader varchar(max) 
DECLARE @Var_TableFoot   varchar(max)
DECLARE @Var_Head        varchar(max)
DECLARE @Var_HTML varchar(max)
DECLARE @Var_DBName varchar(20)
DECLARE @Var_NombreBackup varchar(100)
DECLARE @Var_BackupSizeMB decimal(18,2)=0.00
DECLARE @Var_BackupSize bigint =0
DECLARE @Var_LogMessage varchar(max)
DECLARE @Par_BackupID int



DECLARE @Var_BackupID int
DECLARE @Var_DDSize varchar(20)
DECLARE @Var_DBData varchar(20)
DECLARE @Var_QnaProceso varchar(20)
DECLARE @Var_QnaCerrada varchar(20)
DECLARE @Var_Error varchar(200)
DECLARE @DataBaseSize TABLE
        (
            database_name varchar(20),
            database_size varchar(20),
            unallocated_space varchar(20),
            reserved varchar(20),
            data varchar(20),
            index_size varchar(20),
            unused varchar(20)
        )


SET @Var_BackupSizeMB =0.0
SET @Var_BackupSizeMB=0

SET @Var_DBName='IEEPO' 
SET @Var_Fecha = convert(varchar, getdate()-1, 112)
SET @Var_Archivo = '\\172.16.3.34\E$\Backups\'+@Var_DBName+'_backup_'+ @Var_Fecha +'.bak'
SET @Var_Error='' 
SET @Var_NombreBackup= @Var_DBName+'_backup_'+ @Var_Fecha +'.bak'



-- Insertamos un registro del job de backups

EXEC DB.dbo.[BACKUPNEW] 1,1,@Var_NombreBackup,@Par_BackupID=@Var_BackupID output

SET @Var_LogMessage= concat('Insert New Entry,BACKUPNEW: ', 1,'-',1,'-Var_NombreBackup:',@Var_NombreBackup,'-Par_BackupID:',@Par_BackupID,'-Var_Backup:',@Var_BackupID)
insert into DB.tmp.BACKUPLOG(DateEntry,LogMessage)
Values(getdate(),@Var_LogMessage)

BACKUP DATABASE [IEEPO] TO DISK = @Var_Archivo 
WITH NOFORMAT, NOINIT, NAME = 'IEEPO-Full Database Backup', SKIP, NOREWIND, NOUNLOAD, COMPRESSION,  STATS = 10

-- verificamos si hay registros de error en el backup.

drop table if exists #error_log;

CREATE TABLE #error_log 
	( 
	LogDate datetime, 
	ProcessInfo varchar(100), 
	TextData varchar(max) 
	)




	INSERT INTO #error_log(LogDate, ProcessInfo, TextData)
	EXEC  sys.sp_readerrorlog 0,1,N'Fail','Backup'

	-- 
	--DECLARE @Var_BackupID int =12
	-- DECLARE @Var_Error varchar(max)

	
	SET @Var_Error=(select top 1 left(TextData,200) from #error_log where convert(date,Logdate)=convert(date,getdate())  and TextData like concat('%',@Var_NombreBackup,'%') order by  TextData desc)
	SET @Var_Error=coalesce(@Var_Error,'')
	
	-- SELECT left(@Var_Error,200),@Var_BackupID,len(@Var_Error)
	IF (len(@Var_Error)>1 )
		BEGIN	
			-- EXEC DB.dbo.[BACKUPUPDATE] @Var_BackupID,1, 2,@Var_Error 
			EXEC DB.dbo.[BACKUPUPDATE] @Var_BackupID,1, 2,@Var_Error,1, @Var_NombreBackup, @Var_BackupSizeMB , @Var_BackupSize

            SET @Var_LogMessage= concat('Insert New Entry,BACKUPUPDATE: Var_BackupID:', @Var_BackupID,'-',1,'-',2,'-Var_Error:',@Var_Error,'-',1,'-Var_NombreBackup:',@Var_NombreBackup,'-Var_BackupSizeMB:',@Var_BackupSizeMB,'-Var_BackupSize',@Var_BackupSize)
            insert into DB.tmp.BACKUPLOG(DateEntry,LogMessage)
            Values(getdate(),@Var_LogMessage)

			SET @Var_DBName=@Var_DBName
			SET @Var_DDSize=0.00
			SET @Var_DBData=0.00
			SET @Var_QnaCerrada='----'
			SET @Var_QnaProceso ='----'
		END
	ELSE
		BEGIN
	
			INSERT INTO @DataBaseSize EXEC sp_spaceused @oneresultset = 1  

			SET @Var_DBName = (select database_name from @DataBaseSize)
			SET @Var_DDSize = (select database_size from @DataBaseSize)
			SET @Var_DBData = (select data from @DataBaseSize)
			SET @Var_QnaCerrada = (select top 1 dbo.fechaToAnioQuincena(fechaini) 
									from calennomina where Procesado = 1 and actualizado = 0 and parcial = 0
									)
			SET @Var_QnaProceso = (select dbo.fechaToAnioQuincena(max(fechaini)) 
									from calennomina where procesado = 1 and Actualizado = 1 and Parcial = 0
									)

			-- Informaciòn del backup generado.
			SET @Var_BackupSizeMB 	= (select (compressed_backup_size/1024)/1000 BackupSizeMB from msdb.dbo.backupset where database_name=@Var_DBName and convert(date, backup_start_date)=convert(date,getdate()))
			SET @Var_BackupSize		= (select (compressed_backup_size) BackupSize from msdb.dbo.backupset where database_name=@Var_DBName and convert(date, backup_start_date)=convert(date,getdate()))

			EXEC DB.dbo.[BACKUPUPDATE] @Var_BackupID,1, 1,'Backup generado correctamente.' ,1, @Var_NombreBackup , @Var_BackupSizeMB , @Var_BackupSize
            
            SET @Var_LogMessage= concat('Insert New Entry,BACKUPUPDATE: Var_BackupsID:', @Var_BackupID,'-',1,'-',1,'-Var_Error:','Backup generado correctamente','-',1,'-Var_NombreBackup:',@Var_NombreBackup,'-Var_BackupSizeMB:',@Var_BackupSizeMB,'-Var_BackupSize',@Var_BackupSize)
            insert into DB.tmp.BACKUPLOG(DateEntry,LogMessage)
            Values(getdate(),@Var_LogMessage)


		END








INSERT INTO @DataBaseSize EXEC sp_spaceused @oneresultset = 1  

SET @Var_DBName = (select database_name from @DataBaseSize)
SET @Var_DDSize = (select database_size from @DataBaseSize)
SET @Var_DBData = (select data from @DataBaseSize)
SET @Var_QnaCerrada = (select top 1 dbo.fechaToAnioQuincena(fechaini) 
                        from calennomina where Procesado = 1 and actualizado = 0 and parcial = 0
                        )
SET @Var_QnaProceso = (select dbo.fechaToAnioQuincena(max(fechaini)) 
                        from calennomina where procesado = 1 and Actualizado = 1 and Parcial = 0
                        )
SET @Var_TableRows =(select @Var_DBName [TD] ,@Var_DDSize [TD] ,@Var_DBData [TD], @Var_QnaCerrada [TD] ,@Var_QnaProceso [TD]
      For XML raw('tr'), Elements)
 
SET @Var_Archivo = replace(@Var_Archivo,'\','&#92;') -- backslash
SET @Var_Archivo = replace(@Var_Archivo,'$','&#36;') -- dollar

SET @Var_Head = '<html><head>' + 
                  '<style>' + 
                  'td {padding-left:5px;padding-right:5px;padding-top:5px;padding-bottom:5px;font-family: Arial, Helvetica, sans-serif; font-size: 10pt;} ' + 
                  '</style>' + 
                  '</head>' + 
                  '<body>'+
                  'El respaldo de la BD ' + @Var_DBName +  ' se realizo correctamente' + 
                  '<br>Archivo: ' + @Var_Archivo +
                  '<br>Dir. Local: Directorio E:&#92;Backups ' + 
		  '<br>Detalle:'
                    

SET @Var_TableHeader = '<table cellpadding="5" cellspacing="0" border="1" bordercolor="#C0C0C0" style="font-family: Arial, Helvetica, sans-serif; font-size: 10pt; border-collapse:collapse;border-bottom-style:solid;">' + 
                        '<tr bgcolor=#FFEFD8>' +
                        '<td align=center style="background-color: #E546A5; color:white"><b>Database</b></td>' + 
                        '<td align=center style="background-color: #E546A5; color: white"><b>Tama&#241;o</b></td>' + 
                        '<td align=center style="background-color: #E546A5; color: white"><b>DataFiles</b></td>' +
                        '<td align=center style="background-color: #E546A5; color: white"><b>QnaProceso</b></td>' + 
                        '<td align=center style="background-color: #E546A5; color: white"><b>QnaCerrada</b></td>'; 


SET @Var_TableFoot = '</table><hr></body></html>'; 


SET @Var_HTML = concat(@Var_Head,@Var_TableHeader , @Var_TableRows , @Var_TableFoot)

EXEC msdb.dbo.sp_send_dbmail @profile_name='BackupsBaseDatosIeepo',
    @recipients= 'marart@ieepo.gob.mx;enlace.informatica@ieepo.gob.mx;mcruz@ieepo.gob.mx;sgallardo@ieepo.gob.mx;vjimenezv@ieepo.gob.mx',
    @subject= 'Respaldo de base de datos IEEPO',
    @body_format = 'HTML',
    @body= @Var_HTML 

