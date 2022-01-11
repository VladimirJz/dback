from re import split
from django.shortcuts import render,reverse
from django.contrib import messages
from django.views.generic import ListView,TemplateView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from app.catalog.models import DataBases, Servers, Tables
from app.deploy.models import Jobs
from app.tracking.models import TablesDetail
from django.urls import resolve
from app.catalog.forms import NewServerForm
from core.utils import get_breadcrumb

class DeployJobsListView(TemplateView):
    model=Jobs
    context_object_name ='Jobs_list'
    template_name='deploy/jobs_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        jobs_list=Jobs.objects.all()
    #   tables_list = Tables.objects.filter(DataBase_id=self.kwargs['pk'],DetailOf__DataSizeMB__isnull=False).values('id','Schema','Name','Status','CreateDate','TableCategory__Category','DetailOf__DataSizeMB').order_by('-CreateDate')[:20]
        app='deploy'
        menu='jobs'
        context ['menu']=menu

        context['app']=app
        context['jobs_list']=jobs_list
        current_url = self.request.resolver_match.url_name
        breadcrumb=get_breadcrumb(current_url)
        context['breadcrumb']=breadcrumb
        return context  