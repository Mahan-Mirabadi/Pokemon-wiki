from django.urls import path
from trainers import views
app_name = 'trainers'
urlpatterns=[
    path("register",views.TrainerRegister,name="trainer_register"),
    path("register_thanks",views.RegisterThanks,name="register_thanks"),
    path("login",views.TrainerLogin,name="trainer_login"),
    path("login_thanks",views.LoginThanks,name="login_thanks"),
]