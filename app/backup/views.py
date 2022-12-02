from pipes import Template
from django.shortcuts import redirect, render
from django.views.generic import UpdateView,ListView,TemplateView,FormView
from django.shortcuts import get_object_or_404
from datetime import datetime
from app.backup.models import Backups,Locations
from app.backup.forms import BackupForm,UpdateLostForm
from core.utils import get_breadcrumb
from django.db.models import Avg, Count, Min, Sum
from django.db.models.fields import FloatField
from django.http import HttpResponseNotFound
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from dal import autocomplete
# Create your views here.

class BackupUpdateView(UpdateView):
    model=Backups
    form_class=BackupForm
    template_name='backup/backup_update.html'
    context_object_name='backup_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        app='backup'
        menu='update'
        current_url = self.request.resolver_match.url_name
        breadcrumb=get_breadcrumb(current_url)
        context['breadcrumb']=breadcrumb
        context ['menu']=menu
        context['app']=app
        return context

class BackupLostView(TemplateView): #not
    #model=Backups
    template_name='backup/backup_list.html'
    context_object_name ='backup_list'




    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        form=(request.POST)
        selected_backups=request.POST.getlist("selected")
        selected_location=request.POST.getlist("selected")
        new_location_id=request.POST.get("location")
        new_status_id=request.POST.get("status")
        now=datetime.now()
        comments="Archivo relocalizado manualmente."
        #update
        if(selected_backups):
            Backups.objects.filter(id__in=selected_backups).update(Status=new_status_id,Location=new_location_id,Updated=now,Comments=comments)
        return redirect("backup_lost")


        print(new_location_id,new_status_id)
        

        print(selected_backups)
        print('POST')
        # if context["update_lost_form"].is_valid():
        #     print(context["update_lost_form"])
        #     print('ISVALID')
        #     form=get_object_or_404(context["update_lost_form"])
            

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        update_lost_form = UpdateLostForm(self.request.POST or None)  # instance= None

        backup_list =  Backups.objects.filter(Status__lt=4,Status__gt=2).order_by('-CreationDate')
        app='backup'
        menu='update'
        current_url = self.request.resolver_match.url_name
        breadcrumb=get_breadcrumb(current_url)
        context['breadcrumb']=breadcrumb
        context ['menu']=menu
        context['app']=app
        context['backup_list']=backup_list
        context['update_lost_form']=update_lost_form
        return context

class BackupListView(TemplateView,ListView): #not
    #model=Backups
    template_name='backup/backup_list.html'
    context_object_name ='backup_list'
    paginate_by=10
    queryset = Backups.objects.all()  # Default: Model.objects.all()

    def get_queryset(self):
        print('GET QUERYSET')
        #return Backups.objects.select_related('').order_by('-id')[:30]
        return Backups.objects.select_related('Database').order_by('-id')[:30]

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        #self.object_list = self.get_queryset()
        print(self.object_list)
        print('POST METHOD')
        form=(request.POST)
        selected_backups=request.POST.getlist("selected")
        selected_location=request.POST.getlist("selected")
        new_location_id=request.POST.get("location")
        new_status_id=request.POST.get("status")
        now=datetime.now()
        #update
        if(selected_backups):
            Backups.objects.filter(id__in=selected_backups).update(Status=new_status_id,Location=new_location_id,Updated=now)
        return redirect("backup_update")
            

    def get_context_data(self, **kwargs):
        queryset = kwargs.pop('object_list', None)
        # i dont why object_list is neede if the context_name was overriden, but works
        
        if queryset is None:
            self.object_list = self.get_queryset()
            print('entra aqui')
        context = super().get_context_data(**kwargs)

        #page = self.request.GET.get('page', 1)
        #paginator = Paginator(self.object_list, 40)
        #page_range = paginator.get_elided_page_range(number=page)


        update_lost_form = UpdateLostForm(self.request.POST or None)  # instance= None
        
        # backup_list =  Backups.objects.all().order_by('-CreationDate')[:50]
        # print('OBJECT_LIST)')
        # print(self.object_list)
        # print('GET CONTEXT')
        # print(backup_list)



        app='backup'
        menu='backup'
        current_url = self.request.resolver_match.url_name
        breadcrumb=get_breadcrumb(current_url)
        context['breadcrumb']=breadcrumb
        context ['menu']=menu
        context['app']=app
        #context['backup_list']=backup_list
        context['update_lost_form']=update_lost_form
        return context

class BackupDashView2(TemplateView):
    template_name='backup/line_chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        label=list(Backups.objects.filter(Status=3).values_list('FileName', flat=True))
        data=list(Backups.objects.filter(Status=3).annotate(BackupSize=Sum('SizeMB', output_field=FloatField())).values_list('BackupSize', flat=True))
        context['label']=label
        context['data']=data
        
        return context
    pass

class BackupDashView(TemplateView):
    template_name='backup/backup_stats.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        label=list(Backups.objects.filter(Status=3).values_list('FileName', flat=True))
        data=list(Backups.objects.filter(Status=3).annotate(BackupSize=Sum('SizeMB', output_field=FloatField())).values_list('BackupSize', flat=True))
        context['label']=label
        context['data']=data
        
        return context
    pass


## Locations
# Locations Model.
class LocationListView(ListView):
    model=Locations


class JobScheduleCreate(TemplateView):
    template_name='backup/backup_job_new.html'
    #model=Backups
    #queryset=Backups.objects.all()
    

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        #backups=Backups.objects.filter(Database_id=5).values('id','FileName')
        backups=Backups.objects.all()
        print(self.args)
        context['backups']=backups
        return context

    def post(self,request):
        print ('post')
        context=self.get_context_data()
        print(request.POST)
        print(request.user)
        return self.render_to_response(context=context)

    # def get(self, request, *args, **kwargs):
    #     print('METHOD GET:!!! ')
    #     current_user = request.user
    #     print(current_user.id)
    #     print(request.user)
    
    #    request.context['backups']=Backups.objects.filter(id=current_user.id)

       #WW return super().get(request, *args, **kwargs)

    

class BackupsAutocomplete(autocomplete.Select2QuerySetView):
    
    def get_queryset(self):
        qs=Backups.objects.all()
        if self.q:
            qs=qs.filter(FileName__istartswith=self.q)
        #return super().get_queryset()
        return qs