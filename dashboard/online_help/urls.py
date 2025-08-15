from django.urls import path
from . import views

app_name = 'online_help'
urlpatterns = [  
    # Home and user-related paths
    path('', views.home_test, name='home_test'),
]