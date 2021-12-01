# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app.catalog import views
from app.catalog.views import ServerCreateView, TablesListView 

urlpatterns = [

    # The home page

    path('tables/',TablesListView.as_view()),
    path('servers/new/',ServerCreateView.as_view()),

]
