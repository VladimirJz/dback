from django.shortcuts import render,reverse
from django.views.generic import ListView,TemplateView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from app.catalog.models import Servers, Tables
from app.catalog.forms import NewServerForm

# Create your views here.
class TablesListView(ListView): 
    model=Tables
    context_object_name ='tables_list'
    queryset =  Tables.objects.all().values('id','Schema','Name','CreateDate','TableCategory__Category').order_by('-CreateDate')[:10]

    #queryset =  Backups.objects.filter(Size__isnull=False).values('id','Comments','Location__LocationName','FileName','Size','Comments','CreationDate','Status__Description','Status_id').order_by('-id')

    #template_name='catalog/tables_list.html'
    #paginate_by = 10

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in 
        num_tables=Tables.objects.all().count()
        app='catalog'
        #view='tables'
        context ['app']=app
        #context['view']=view
        context['num_tables']= num_tables
        self.template_name = 'catalog/tables_list.html'
        return context

#def create_server(request):
#    form = NewServerForm()
#    return render(request, 'blog/post_edit.html', {'form': form})


# SERVERS
class ServerListView(ListView): #not
    model=Servers
    template_name='catalog/servers_list.html'
    context_object_name ='servers_list'
    queryset =  Servers.objects.all().values('id','Server','Host','Instance','Port','Type','Environment','Status')


    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in 
    
        app='catalog'
        #view='servers'
        context ['app']=app
        #context['view']=view
        # context['num_tables']= num_tables

        return context

class ServerDetailView(DetailView):
    model = Servers

    template_name='catalog/servers_detail.html'
    context_object_name = 'server_detail'


class ServerUpdateView(UpdateView):
    model = Servers
    form_class = NewServerForm
    context_object_name="server_update"
    #fields = ('__all__')
    template_name='catalog/servers_update.html'
    #template_name_suffix = '_update_form'
    success_url = "/servers/update/1"
    success_message = "Server %(Server)s was update successfully"

class ServerCreateView(SuccessMessageMixin,CreateView):#not
    model = Servers
    template_name = 'catalog/servers_new.html'
    context_object_name="server_create"

    form_class = NewServerForm
    #fields = '__all__'
    success_url = "/servers/new/"
    success_message = "Server %(Server)s was registered successfully"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in     
        app='catalog'
        #view='servers'
        go_back='/servers/'
        context ['app']=app
        #context['view']=view
        context['go_back']=go_back
        # context['num_tables']= num_tables
        return context

class ServerDeleteView(SuccessMessageMixin,DeleteView):
    # specify the model you want to use
    model = Servers
    context_object_name="server_delete"
    template_name = 'catalog/servers_delete.html'
    # can specify success url
    # url to redirect after successfully
    # deleting object
    success_url ="/servers/"
    success_message = "Server %(Server)s was deleted"