
-- ------------------------------
--  STEP : 1 
-- ------------------------------


DECLARE @BACKUPJOBID int;
DECLARE @TAGBACKUP		varchar(12);
DECLARE @SUCCESS_BACKUP_MESSAGE varchar(300);

-- ||||||||||||||||||||||||||||||||||||
-- -- -- --- -- - -- -- -- - -- - - -
SET @BACKUPJOBID= 1; --  <-- SET Job_id 
SET @TAGBACKUP='DAILYBACKUP';
SET @SUCCESS_BACKUP_MESSAGE='Successfully generated backup'
-- - -- -- - -- - - -- - - -- - - - -
--||||||||||||||||||||||||||||||||||||

DECLARE @LOCATIONID		int;
DECLARE @FILENAME		varchar(300);
DECLARE @DATABASENAME	varchar(30);
DECLARE @DATABASEID		int;
DECLARE @JOBNAME		varchar(30);
DECLARE @CURRENTDATETIME	datetime;
DECLARE @CURRENTDATE	datetime;
DECLARE @LOCATIONNAME	varchar(30);
DECLARE @REMOTEPATH		varchar(200);
DECLARE @BACKUPPATH		varchar(200);
DECLARE @FILESPATH		varchar(200);
DECLARE @FULLFILENAME   varchar(300);
DECLARE @ISLOCAL		bit;
DECLARE @BACKUPDATE		varchar(12);
DECLARE @BACKUPID		int;	
DECLARE @BACKUPNAME		varchar(300);
DECLARE @BACKUPERROR	varchar(max);
DECLARE @BACKUPSIZE		bigint;
DECLARE @BACKUPSIZEMB	decimal(18,2)=0.00
DECLARE @SECUENCE		int;
-- 
DECLARE @BACKUP_WAS_NOT_GENERATED int;
DECLARE @EMPTY int;
DECLARE @BACKUP_SUCCESSFULLY int;
SET @BACKUP_SUCCESSFULLY=1;
SET @BACKUP_WAS_NOT_GENERATED=2;
SET @EMPTY=0

-- 


SET @CURRENTDATETIME=getdate();
SET @CURRENTDATE=convert(date,@CURRENTDATETIME)
SET @BACKUPDATE=convert(varchar, getdate()-1, 112);

SELECT  @LOCATIONNAME=LocationName, @JOBNAME=JobName,		@DATABASENAME=[Database],
		@REMOTEPATH=RemotePath,		@FILESPATH=FilesPath,	@ISLOCAL=IsLocal,
		@DATABASEID=Database_id,	@LOCATIONID=bl.id

	from 
	dba..backup_locations bl inner join (
	dba..backup_jobs bj inner join dba..catalog_databases db on bj.Database_id=db.id)
	on bl.id=bj.location_id 
	where bj.id=@BACKUPJOBID;




SET @BACKUPNAME=CONCAT(@DATABASENAME,' ',@TAGBACKUP,' ','BACKUP');

SET @BACKUPPATH= CASE WHEN @ISLOCAL=0 THEN @REMOTEPATH ELSE @FILESPATH END;


SET @FILENAME= concat(@DATABASENAME,'_', coalesce(@TAGBACKUP,'BACKUP'),'-',@BACKUPDATE)
SET @SECUENCE= (SELECT count(*) from backup_files where CreationDate=@CURRENTDATE and FileName like concat(@FILENAME,'%'))
IF(@SECUENCE>@EMPTY)
BEGIN
	SET @FILENAME=concat(@FILENAME,'-',cast(@SECUENCE as varchar ))
END

SET @FILENAME=concat(@FILENAME,'.bak') --  TODO: add the extension on model	
SET @FULLFILENAME=concat(@BACKUPPATH,@FILENAME)


--


INSERT INTO [dbo].[backup_files]
           ([Database_id],	[Job_id],		[CreationDate],	[StartBackup],		[FileName],
		   [Location_id])
	VALUES (@DATABASEID,		@BACKUPJOBID,	@CURRENTDATE,	@CURRENTDATETIME,	@FILENAME,
			@LOCATIONID);

SET @BACKUPID=(SELECT SCOPE_IDENTITY())

-- launch backup
BACKUP DATABASE @DATABASENAME TO DISK = @FULLFILENAME 
WITH NOFORMAT, NOINIT, NAME =@BACKUPNAME , SKIP, NOREWIND, NOUNLOAD, COMPRESSION,  STATS = 10;

SET @CURRENTDATETIME=getdate();

-- simple lookup for a backup-error on logs 
drop table if exists dba..#error_log;
CREATE TABLE dba..#error_log 
	( 
	LogDate datetime, 
	ProcessInfo varchar(100), 
	TextData varchar(max) 
	);

INSERT INTO #error_log(LogDate, ProcessInfo, TextData)
	EXEC  sys.sp_readerrorlog 0,1,N'Fail','Backup';

SET @BACKUPERROR=(select top 1 left(TextData,200) from #error_log where convert(date,Logdate)=convert(date,getdate())  and TextData like concat('%',@FILENAME,'%') order by  TextData desc)
SET @BACKUPERROR=coalesce(@BACKUPERROR,'')
IF (len(@BACKUPERROR)>1 )
	BEGIN	

			UPDATE dba.[dbo].[backup_files] 
			SET
			Status_id=@BACKUP_WAS_NOT_GENERATED,
			Comments=@BACKUPERROR,
			EndBackup=@CURRENTDATETIME,
			Size=@EMPTY,
			SizeMB=@EMPTY
		WHERE id=@BACKUPID
	END
ELSE
	BEGIN
		SET @BACKUPSIZEMB 	= (select top 1 (compressed_backup_size/1024)/1000 BackupSizeMB from msdb.dbo.backupset where database_name=@DATABASENAME and convert(date, backup_start_date)=convert(date,getdate()) order by backup_start_date desc)
		SET @BACKUPSIZE		= (select  top 1 (compressed_backup_size) BackupSize from msdb.dbo.backupset where database_name=@DATABASENAME and convert(date, backup_start_date)=convert(date,getdate())order by backup_start_date desc)
		print(@BACKUPSIZEMB)
		UPDATE dba.[dbo].[backup_files] 
		SET
			Status_id=@BACKUP_SUCCESSFULLY,
			Comments=@SUCCESS_BACKUP_MESSAGE,
			EndBackup=@CURRENTDATETIME,
			Size=@BACKUPSIZE,
			SizeMB=@BACKUPSIZEMB
		WHERE id=@BACKUPID
	END 
            



## to Copy  to dba database

select concat('INSERT INTO dba..backup_files (CreationDate,StartBackup,EndBackup,FileName,SizeMB,Size,Comments,Database_id,Job_id,Status_id) VALUES (',
'''',CreationDate,''',''',convert(varchar,StartBackup, 21),''',''',convert(varchar,EndBackup,21),''',''',FileName,''',',BackupSize,',',BackupSizeMB,',''',Comments,''',',DataBaseID,',',BackupJobID,',',
LocationID,',',BackupStatusID,')')
from 
DB..BACKUPS

select concat('INSERT INTO dba..backup_files (CreationDate,StartBackup,EndBackup,FileName,SizeMB,Size,Comments,Database_id,Job_id,Location_id,Status_id) VALUES (',
'''',CreationDate,''',''',convert(varchar,StartBackup, 21),''',''',convert(varchar,EndBackup,21),''',''',FileName,''',',BackupSize,',',BackupSizeMB,',''',replace(Comments,'''',''),''',',DataBaseID,',',BackupJobID,',',
LocationID,',',BackupStatusID,')')
from 
DB..BACKUPS