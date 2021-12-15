
# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app.catalog import views
from app.tracking.views import TablesDetailView


urlpatterns = [

    # The home page

    path('tables/detail/<int:pk>', TablesDetailView.as_view(),name='tabledetail'),



]
