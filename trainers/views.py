from django.shortcuts import render, redirect
from . forms import TrainerRegisterForm,TrainerLoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages 

# Create your views here.
def TrainerRegister(request):
    if request.method == 'POST':  # Check request method here
        form_register = TrainerRegisterForm(request.POST)
        if form_register.is_valid():
            data = form_register.cleaned_data
            User.objects.create_user(username=data['trainer_name'], email=data['email'], password=data['password_2'])
            return redirect('trainers:register_thanks')
    else:
        form_register = TrainerRegisterForm()  # Create an empty form for GET requests
    context = {'form_register': form_register}
    return render(request, 'trainers/trainer_register.html', context=context)
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def RegisterThanks (request):
    return render(request, 'trainers/register_thanks.html')
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def TrainerLogin(request):
    if request.method == 'POST':
        form_login = TrainerLoginForm(request.POST)
        if form_login.is_valid():
            data = form_login.cleaned_data
            user = authenticate(username=data['trainer_name'], password=data['password'])  # Use trainer_name for authentication
            if user is not None:
            # Check if the authenticated user is a trainer (assuming logic)
                if isinstance(user, User):  # Replace 'Trainer' with your actual model name
                    login(request, user)
                    return redirect('trainers:login_thanks')
                else:
                    messages.error(request, 'Invalid trainer credentials')  # Specific error message for trainers
        else:
            messages.error(request, 'Invalid username or password') 
    else:
        form_login = TrainerLoginForm() 
    context = {'form_login': form_login}# Generic error message
    return render(request, 'trainers/trainer_login.html')  # Replace 'login.html' with your trainer login template
#................................................
def LoginThanks (request):
    return render(request, 'trainers/login_thanks.html')