
from django.urls import path, re_path
from app.deploy.views import DeployJobsListView

urlpatterns = [

    # The home page

    path('deploy/',DeployJobsListView.as_view(),name='deploy'), #serverlist
 
]
