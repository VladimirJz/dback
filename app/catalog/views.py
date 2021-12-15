from re import split
from django.shortcuts import render,reverse
from django.contrib import messages
from django.views.generic import ListView,TemplateView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from app.catalog.models import DataBases, Servers, Tables
from app.tracking.models import TablesDetail
from django.urls import resolve
from app.catalog.forms import NewServerForm
from core.utils import get_breadcrumb

# Create your views here.
class TablesListVieww(ListView): 
    model=Tables
    context_object_name ='tables_list'
    query_set = Tables.objects.values('id','Schema','Name','Status','CreateDate','TableCategory__Category','DetailOf__DataSizeMB')
    #query_set = Tables.objects.prefetch_related('TablesDetail_set').all()
   # ModelA.objects.prefetch_related('modelb_set').all()
    #query='select  * from [catalog_tablecategory] c inner join ([tracking_tablesdetail]d inner join  [catalog_tables] t on t.id=d.table_id )on c.id=t.TableCategory_id'
    #query_set=Tables.objects.raw(query)
    template_name='catalog/tables_list.html'
    #paginate_by = 10

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in 
        app='catalog'
        menu='tables'
        context ['menu']=menu
        context['app']=app
        return context


class TablesListView(TemplateView):
    model=Tables
    context_object_name ='tables_list'
    #query_set = Tables.objects.all().values('id','Schema','Name','Status','CreateDate','TableCategory__Category','DetailOf__DataSizeMB')
    template_name='catalog/tables_list.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in 
        tables_list = Tables.objects.filter(DataBase_id=self.kwargs['pk'],DetailOf__DataSizeMB__isnull=False).values('id','Schema','Name','Status','CreateDate','TableCategory__Category','DetailOf__DataSizeMB').order_by('-CreateDate')[:20]
        app='catalog'
        menu='tables'
        context ['menu']=menu
        #current_url = resolve(self.request.url_name)

        context['app']=app
        context['tables_list']=tables_list
        #context['current_url']=current_url
        return context  

    #def get_queryset(self):

        #queryset = Tables.objects.all().values('id','Schema','Name','Status','CreateDate','TableCategory__Category','DetailOf__DataSizeMB')



# SERVERS
class ServerListView(ListView): #not
    model=Servers
    template_name='catalog/servers_list.html'
    context_object_name ='servers_list'
    queryset =  Servers.objects.all().values('id','Server','Host','Instance','Port','Type','Environment','Status')


    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        app='catalog'
        menu='servers'
        context ['menu']=menu
        context['app']=app
        return context

class ServerDetailView(DetailView):
    model = Servers
    template_name='catalog/servers_detail.html'
    context_object_name = 'server_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        app='catalog'
        menu='servers'
        go_back='#'
        context ['menu']=menu
        context['app']=app
        context['go_back']=go_back
        return context


class ServerUpdateView(SuccessMessageMixin,UpdateView):
    model = Servers
    form_class = NewServerForm
    context_object_name="server_update"
    template_name='catalog/servers_update.html'
    success_message = "Server %(Server)s was update successfully"

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            app='catalog'
            menu='servers'
            #go_back='#'
            context ['menu']=menu
            context['app']=app
            #context['go_back']=go_back



            return context

class ServerCreateView(SuccessMessageMixin,CreateView):
    model = Servers
    template_name = 'catalog/servers_new.html'
    context_object_name="server_create"
    form_class = NewServerForm
    success_message = "Server %(Server)s was registered successfully"
    success_url = "/servers/new/"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        app='catalog'
        menu='servers'
        context ['menu']=menu
        context['app']=app

        go_back='/servers/'
        #context['view']=view
        context['go_back']=go_back
        # context['num_tables']= num_tables
        return context

class ServerDeleteView(SuccessMessageMixin,DeleteView):
    # specify the model you want to use
    model = Servers
    context_object_name="server_delete"
    template_name = 'catalog/servers_delete.html'
    success_url ="/servers/"
    success_message = "The Server selected was deleted permanently."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        app='catalog'
        menu='servers'
        go_back='#'
        context ['menu']=menu
        context['app']=app
        context['go_back']=go_back
        return context

# DATABASES

class DataBaseListView(ListView): 
    model=DataBases
    template_name='catalog/databases_list.html'
    context_object_name ='databases_list'
    queryset =  DataBases.objects.all().values('id','Database','FriendlyName','Description','CreateDate','DataSizeMB','TablesNum','Server')
   

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        app='catalog'
        menu='databases'
        #current_url = resolve(self.request.url_name)
        current_url = self.request.resolver_match.url_name
        #current_url ='uno_dos_tres_cuatro'
        #breadcrum=current_url.split('_')
        #choices=dict(item.split("=") for item in current_url.split("_"))

        # choices=current_url.split("_")
        # breadcrumb = dict()
        # for i, option in enumerate(choices):
        #     breadcrumb[i] = option

        #choices = {'key1':'val1', 'key2':'val2'}
        breadcrumb=get_breadcrumb(current_url)
        context['current_url']=current_url
        context ['menu']=menu
        context['app']=app
       # context['choices']=choices
        context['breadcrumb']=breadcrumb
        return context