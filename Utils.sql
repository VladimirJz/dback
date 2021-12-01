/****** Script for SelectTopNRows command from SSMS  ******/
SELECT TOP (1000) [TableCategoryID]
      ,[TableCategory]
      ,[Description]
  FROM [DBPROD].[dbo].[TABLESCATEGORY]


  select * from dba.dbo.catalog_tablecategory

  select CONCAT('insert into dba.dbo.catalog_tablecategory(Category) VALUES(''',TableCategory,''')')
     FROM [DBPROD].[dbo].[TABLESCATEGORY] where TableCategoryID>0

  id,Category

  insert into dba.dbo.catalog_tablecategory(Category) VALUES('Administracion')
insert into dba.dbo.catalog_tablecategory(Category) VALUES('Configuracion')
insert into dba.dbo.catalog_tablecategory(Category) VALUES('Catalogo_fijo')
insert into dba.dbo.catalog_tablecategory(Category) VALUES('Catalogo_variable')
insert into dba.dbo.catalog_tablecategory(Category) VALUES('Historica_Maestro')
insert into dba.dbo.catalog_tablecategory(Category) VALUES('Historica_Detalle')
insert into dba.dbo.catalog_tablecategory(Category) VALUES('Plantilla_Reporte')
insert into dba.dbo.catalog_tablecategory(Category) VALUES('Temporal_Trabajo')
insert into dba.dbo.catalog_tablecategory(Category) VALUES('Transaccional_Maestro')
insert into dba.dbo.catalog_tablecategory(Category) VALUES('Transaccional_Detalle')

-- TABLES

select * from DBPROD.obj.TABLES

select * from  dba.dbo.catalog_tables

SELECT CONCAT('INSERT INTO dba.dbo.catalog_tables([Schema],[Name],[ObjectID],[CreateDate],[Status],[TableCategory_id],[DataBase_id]) VALUES(''',

 SchemaDB,''',''',replace(TableName,'''',''),''',''',IDObjectDB,''',''',CreateDate,''',',1,',',coalesce(TableCategoryID,0)+1,',',1,');')
from  DBPROD.obj.TABLES