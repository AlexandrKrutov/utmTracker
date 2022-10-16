from django.urls import path
from .views import *
from .models import UserName

urlpatterns = [
    path('', utm_check, name='index'),
    path(r'user/', miniUserAuth, name='user'),
    path(r'user/projects/', createProject, name='projects'),
    path(r'user/projects/delete/<int:id>/', deleteProject),
    path(r'user/projects/setup/<int:id>/', setUpProject, name='utms'),
    path(r'user/projects/setup/<int:id>/delete/<str:utm_campaign>/', deleteUTM),
]
