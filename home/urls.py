from django.urls import path
from home import views
app_name = 'home'
urlpatterns=[
    path("home/",views.ViewHome,name="view_home"),
    path("about/",views.About,name='about'),
]
