# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app.backup.views import BackupUpdateView,BackupLostView,BackupListView,BackupDashView,LocationListView,JobScheduleCreate, BackupsAutocomplete


urlpatterns = [

    # The home page

    path('backup/',BackupListView.as_view(),name='backup'), #must
    path('backup/lost/',BackupLostView.as_view(),name='backup_lost'),
    path('backup/update/<int:pk>', BackupUpdateView.as_view(),name='backup_update'), #
    path('backup/stats/',BackupDashView.as_view(),name='backup_dashboard'),
    path('backup/dashboard/',BackupDashView.as_view(),name='backup_dashboard'),
    path('backup/locations/', LocationListView.as_view(),name='backup_locations' ),
    path('backup/jobs/new', JobScheduleCreate.as_view(),name='backup_jobs_new' ),
    #path('backup/backup-autocomplete/$', BackupsAutocomplete.as_view(),name='backup-autocomplete'),
    re_path(r'^backup-autocomplete/$',BackupsAutocomplete.as_view(),name='backup-autocomplete',
    ),


]
