

def get_breadcrumb(view_name):
    choices=view_name.split("_")
    path=''
    breadcrumb = dict()
    items=(len(choices)-1)
    for i, option in enumerate(choices):
        #path=path + option + '_'
        #breadcrumb[path[:-1]] = option
        if i==items:
            path='#_'
        else:
            path=path+option+'_'
        breadcrumb[path[:-1]]=option
    return breadcrumb



    
  insert into [deploy_tablefilters]([Column],FilterType,LowerValue,UpperValue,ValuesDataType,StepBy,Table_id)
  values('Id_Periodo',1,3068,3495,1,1,1238)

  insert into [deploy_tablefilters]([Column],FilterType,LowerValue,UpperValue,ValuesDataType,StepBy,Table_id)
  select 'Id_Periodo',1,3068,3495,1,1,id from catalog_tables where [name] in ('histpagosdetalle','Recalculo_histpagos','Folio_Recibos','RastreoImpuesto','nom_histpagos','Hvectores')

  insert into [deploy_tablefilters]([Column],FilterType,LowerValue,UpperValue,ValuesDataType,StepBy,Table_id)
  select  '',0,'','','',0,id from catalog_tables  where TableCategory_id>1 and id not in(select id from catalog_tables c where [name] in ('histpagosdetalle','Recalculo_histpagos','Folio_Recibos','RastreoImpuesto','nom_histpagos','Hvectores'))


    insert into deploy_tablefilters_Job(tablefilters_id,jobs_id) 
	select id,1 from [deploy_tablefilters]



		   truncate table [deploy_jobscripts]
