# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app.catalog import views
from app.catalog.views import ServerCreateView, ServerListView, ServerDetailView, ServerUpdateView, TablesListView ,ServerDeleteView


urlpatterns = [

    # The home page

    path('tables/',TablesListView.as_view()),
    path('servers/',ServerListView.as_view(template_name='catalog/servers_list.html'),name='servers_list'),
    path('servers/new/',ServerCreateView.as_view()),
    path('servers/detail/<int:pk>', ServerDetailView.as_view(), name="server_details"),
    path('servers/update/<int:pk>',ServerUpdateView.as_view(),name="server_update"),
    path('servers/delete/<int:pk>', ServerDeleteView.as_view(),name="server_delete"),
    

]
