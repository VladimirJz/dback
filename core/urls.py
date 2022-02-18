# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include  # add this
from django.conf.urls import include, url
import notifications.urls
admin.site.site_header = 'IEEPO - INFRAESTRUCTURA'                    # default: "Django Administration"
admin.site.index_title = 'DBA'                 # default: "Site administration"
admin.site.site_title = 'ADMIN' # default: "Django site admin"

urlpatterns = [
    path('admin/', admin.site.urls),
   

    url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),

    path("", include("authentication.urls")),  # add this
    path("", include("app.urls")),  # add this
    path("", include("app.catalog.urls"))  ,
    path("", include("app.tracking.urls")),
    path("", include("app.deploy.urls")),
    path("",include("app.inventory.urls")),
]
