from django.shortcuts import render
# Create your views here.
from django.shortcuts import render,reverse
from django.contrib import messages
from django.views.generic import ListView,TemplateView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from app.catalog.models import  Servers, Tables
from app.tracking.models import TablesDetail
from app.catalog.forms import NewServerForm

class TablesDetailView(DetailView):
    model = TablesDetail
    template_name='tracking/tables_detail.html'
    context_object_name = 'table_detail'
    queryset = TablesDetail.objects.values('Table_id','Table__Name','CurrentDate','LastAccess','DataSizeMB','IndexSizeMB','RowsNum','FKeysNum','IndexNum','IndexReads','IndexUpdates','Table__TableCategory__Category','Table__CreateDate')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        app='traking'
        menu='tables'
        go_back='#'
        context ['menu']=menu
        context['app']=app
        context['go_back']=go_back
        return context
