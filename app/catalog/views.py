from django.shortcuts import render
from django.views.generic import ListView,TemplateView,DetailView,CreateView
from app.catalog.models import Servers, Tables
from app.catalog.forms import NewServerForm

# Create your views here.
class TablesListView(ListView):
    model=Tables
    context_object_name ='tables_list'
    queryset =  Tables.objects.all().values('id','Schema','Name','CreateDate','TableCategory__Category').order_by('-CreateDate')[:10]

    #queryset =  Backups.objects.filter(Size__isnull=False).values('id','Comments','Location__LocationName','FileName','Size','Comments','CreationDate','Status__Description','Status_id').order_by('-id')

    template_name='catalog/tables_list.html'
    #paginate_by = 10

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in 
        num_tables=Tables.objects.all().count()
        app='catalog'
        view='tables'
        context ['app']=app
        context['view']=view
        context['num_tables']= num_tables

        return context

#def create_server(request):
#    form = NewServerForm()
#    return render(request, 'blog/post_edit.html', {'form': form})

class ServerCreateView(CreateView):
    model = Servers
    template_name = 'catalog/servers_new.html'
    #fields = '__all__'
    success_url = "/create"
    form_class = NewServerForm
