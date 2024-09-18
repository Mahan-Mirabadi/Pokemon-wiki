from django.urls import path
from trainers import views


app_name = 'trainers'
urlpatterns=[
    path("register/",views.TrainerRegister,name="trainer_register"),
    path("login/",views.TrainerLogin,name="trainer_login"),
    path('logout/', views.LogoutTrainer, name='logout_trainer'),
    path('change_password/', views.change_password, name='change_password'),
]