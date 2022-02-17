from re import split
from django.shortcuts import render,reverse
from django.contrib import messages
from django.views.generic import ListView,TemplateView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from app.tracking.models import TablesDetail
from django.urls import resolve

from core.utils import get_breadcrumb
from app.inventory.models import Item

 

class ItemListView(TemplateView):
    model=Item
    context_object_name ='items_list'
    template_name='inventory/items_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items_list =  Item.objects.values("id","Employ__Name","Employ__LastName","Description","Category__CategoryName","Condition__ConditionName","Status__StatusName")
        app='inventory'
        menu='dashboard'
        context ['menu']=menu
        context['app']=app
        context['items_list']=items_list
        current_url = self.request.resolver_match.url_name
        breadcrumb=get_breadcrumb(current_url)
        context['breadcrumb']=breadcrumb
        return context  