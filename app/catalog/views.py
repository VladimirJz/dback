from notifications.signals import notify
from django.contrib.auth.models import User

from re import split
from django.shortcuts import render,reverse
from django.contrib import messages
from django.views.generic import ListView,TemplateView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from app.catalog.models import DataBases, Servers, Tables,Credentials
from app.tracking.models import TablesDetail
from django.urls import resolve
from app.catalog.forms import NewServerForm,NewDataBaseForm, NewCredentialForm
from core.utils import get_breadcrumb


# Create your views here.
class TablesListVieww(ListView): 
    model=Tables
    context_object_name ='tables_list'
    query_set = Tables.objects.values('id','Schema','Name','Status','CreateDate','TableCategory__Category','DetailOf__DataSizeMB')
    template_name='catalog/tables_list.html'
    #paginate_by = 10

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in 
        app='catalog'
        menu='tables'
        current_url = self.request.resolver_match.url_name
        breadcrumb=get_breadcrumb(current_url)
        context['breadcrumb']=breadcrumb
        context ['menu']=menu
        context['app']=app
        return context


class TablesListView(TemplateView):
    model=Tables
    context_object_name ='tables_list'
    template_name='catalog/tables_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tables_list = Tables.objects.filter(DataBase_id=self.kwargs['pk'],DetailOf__DataSizeMB__isnull=False).values('id','Schema','Name','Status','CreateDate','TableCategory__Category','DetailOf__DataSizeMB').order_by('-CreateDate')[:20]
        app='catalog'
        menu='tables'
        context ['menu']=menu

        context['app']=app
        context['tables_list']=tables_list
        current_url = self.request.resolver_match.url_name
        breadcrumb=get_breadcrumb(current_url)
        context['breadcrumb']=breadcrumb
        return context  


# SERVERS
class ServerListView(ListView): #not
    model=Servers
    template_name='catalog/servers_list.html'
    context_object_name ='servers_list'
    #queryset =  Servers.objects.all().values('id','Server','Host','Instance','Port','Type','Environment','Status')



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        app='catalog'
        menu='servers'
        current_url = self.request.resolver_match.url_name
        breadcrumb=get_breadcrumb(current_url)
        context['breadcrumb']=breadcrumb
        context ['menu']=menu
        context['app']=app
        return context



class CredentialListView(ListView):
    model=Credentials
    template_name='catalog/credentials_list.html'
    context_object_name ='credential_list'
    #queryset =  DataBases.objects.all().values('id','Database','FriendlyName','Description','CreateDate','DataSizeMB','TablesNum','Server')
   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        app='catalog'
        menu='credentials'
        current_url = self.request.resolver_match.url_name
        breadcrumb=get_breadcrumb(current_url)
        context['breadcrumb']=breadcrumb
        context['current_url']=current_url
        context['menu']=menu
        context['app']=app
       # context['choices']=choices
        return context




class ServerDetailView(DetailView):
    model = Servers
    template_name='catalog/servers_detail.html'
    context_object_name = 'server_detail'
    #queryset=Servers.objects.all().values('id','Server','Host','get_Type_display','Port','Instance')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        app='catalog'
        menu='servers'
        go_back='#'
        current_url = self.request.resolver_match.url_name
        breadcrumb=get_breadcrumb(current_url)
        context['breadcrumb']=breadcrumb
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
    u = User.objects.get(username='vladimir')
    #notify.send(u, recipient=u, verb='you reached level 16 ',message='actualizado')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        app='catalog'
        menu='servers'
        current_url = self.request.resolver_match.url_name
        breadcrumb=get_breadcrumb(current_url)
        context['breadcrumb']=breadcrumb
        context ['menu']=menu
        context['app']=app
        return context

class ServerCreateView( SuccessMessageMixin,CreateView):
    model = Servers
    template_name = 'catalog/servers_new.html'
    context_object_name="server_create"
    form_class = NewServerForm
    u = User.objects.get(username='vladimir')
    #count=Notification.objects.all().count()
    success_message = "Server %(Server)s was registered successfully"
    success_url = "/servers/new/"
   # notify.send(u, recipient=u, verb='you reached level 16  ')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        app='catalog'
        menu='servers'
        current_url = self.request.resolver_match.url_name
        breadcrumb=get_breadcrumb(current_url)
        context['breadcrumb']=breadcrumb
        context ['menu']=menu
        context['app']=app

        go_back='/servers/'
        context['go_back']=go_back
        return context


class CredentialCreateView( SuccessMessageMixin, CreateView):
    model=Credentials
    template_name= 'catalog/credentials_new.html'
    form_class=NewCredentialForm



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
        current_url = self.request.resolver_match.url_name
        breadcrumb=get_breadcrumb(current_url)
        context['breadcrumb']=breadcrumb
        context ['menu']=menu
        context['app']=app
        context['go_back']=go_back
        return context

# DATABASES

class DataBaseListView(ListView): 
    model=DataBases
    template_name='catalog/databases_list.html'
    context_object_name ='databases_list'
    #queryset =  DataBases.objects.all().values('id','Database','FriendlyName','Description','CreateDate','DataSizeMB','TablesNum','Server')
   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        app='catalog'
        menu='databases'
        current_url = self.request.resolver_match.url_name
        breadcrumb=get_breadcrumb(current_url)
        context['breadcrumb']=breadcrumb
        context['current_url']=current_url
        context['menu']=menu
        context['app']=app
       # context['choices']=choices
        return context


class DataBaseCreateView(SuccessMessageMixin,CreateView):
    model=DataBases
    form_class=NewDataBaseForm
    template_name='catalog/databases_new.html'
    success_url= "/servers/databases/new"
 
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            app='catalog'
            menu='databases'
            current_url = self.request.resolver_match.url_name
            breadcrumb=get_breadcrumb(current_url)
            context['breadcrumb']=breadcrumb
            context ['menu']=menu
            context['app']=app

            go_back='/servers/databases/'
            context['go_back']=go_back
            return context
