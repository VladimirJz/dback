# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app.catalog import views
from app.catalog.views import DataBaseListView,DataBaseCreateView, ServerCreateView, ServerListView, ServerDetailView, ServerUpdateView, TablesListView ,ServerDeleteView,CredentialListView,CredentialCreateView


urlpatterns = [

    # The home page

    path('servers/',ServerListView.as_view(template_name='catalog/servers_list.html'),name='servers'), #serverlist
    path('servers/new/',ServerCreateView.as_view(),name='servers_new'),#servernew
    path('servers/detail/<int:pk>', ServerDetailView.as_view(), name="servers_details"),#serverdetails
    path('servers/update/<int:pk>',ServerUpdateView.as_view(),name="servers_update"),#catalog_serverupdate
    path('servers/delete/<int:pk>', ServerDeleteView.as_view(),name="servers_delete"),#serverdelete
    path('servers/databases/',DataBaseListView.as_view(),name='servers_databases'),#catalog_databaseslist
    path('servers/databases/new/',DataBaseCreateView.as_view(),name='servers_databases_new'),
    path('servers/credentials/',CredentialListView.as_view(), name='servers_credentials'),
    path('servers/credentials/new', CredentialCreateView.as_view(), name='servers_credentials_new'),
    path('databases/',DataBaseListView.as_view(),name='tracking'),#tracking_databaseslist
    path('databases/<int:pk>',TablesListView.as_view(),name='servers_databases_details'),#tableslist


]
