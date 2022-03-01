from pipes import Template
from django.shortcuts import redirect, render
from django.views.generic import UpdateView,ListView,TemplateView,FormView
from django.shortcuts import get_object_or_404
from datetime import datetime
from app.backup.models import Backups
from app.backup.forms import BackupForm,UpdateLostForm
from core.utils import get_breadcrumb
from django.db.models import Avg, Count, Min, Sum
from django.db.models.fields import FloatField
# Create your views here.

class BackupUpdateView(UpdateView):
    model=Backups
    form_class=BackupForm
    template_name='backup/backup_update.html'

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

class BackupListView(TemplateView): #not
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
        #update
        if(selected_backups):
            Backups.objects.filter(id__in=selected_backups).update(Status=new_status_id,Location=new_location_id,Updated=now)
        return redirect("backup_update")


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

        backup_list =  Backups.objects.all().order_by('-CreationDate')
        app='backup'
        menu='backup'
        current_url = self.request.resolver_match.url_name
        breadcrumb=get_breadcrumb(current_url)
        context['breadcrumb']=breadcrumb
        context ['menu']=menu
        context['app']=app
        context['backup_list']=backup_list
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