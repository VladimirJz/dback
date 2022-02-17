# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app.inventory.views  import ItemListView


urlpatterns = [

    # The home page

    path('inventory/', ItemListView.as_view(),name='inventory'), #serverlist



]
