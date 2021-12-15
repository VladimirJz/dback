# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app.catalog import views
from app.catalog.views import DataBaseListView, ServerCreateView, ServerListView, ServerDetailView, ServerUpdateView, TablesListView ,ServerDeleteView


urlpatterns = [

    # The home page

    path('servers/',ServerListView.as_view(template_name='catalog/servers_list.html'),name='serverslist'),
    path('servers/new/',ServerCreateView.as_view(),name='servernew'),
    path('servers/detail/<int:pk>', ServerDetailView.as_view(), name="serverdetails"),
    path('servers/update/<int:pk>',ServerUpdateView.as_view(),name="catalog_serverupdate"),
    path('servers/delete/<int:pk>', ServerDeleteView.as_view(),name="serverdelete"),
    path('servers/database/',DataBaseListView.as_view(),name='catalog_databaseslist'),
    path('databases/',DataBaseListView.as_view(),name='tracking_databaseslist'),

    path('databases/<int:pk>',TablesListView.as_view(),name='tableslist'),


]
