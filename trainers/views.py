from django.shortcuts import render, redirect
from . forms import TrainerRegisterForm,TrainerLoginForm,CustomPasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages 
# Create your views here.
def TrainerRegister(request):
    if request.method == 'POST': 
        form_register = TrainerRegisterForm(request.POST)
        if form_register.is_valid():
            data = form_register.cleaned_data
            User.objects.create_user(username=data['trainer_name'], email=data['email'], password=data['password_2'])
            return render(request, 'trainers/register_thanks.html')
    else:
        form_register = TrainerRegisterForm()  
    context = {'form_register': form_register}
    return render(request, 'trainers/trainer_register.html', context=context)
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def TrainerLogin(request):
    if request.method == 'POST':
        form_login = TrainerLoginForm(request.POST)
        if form_login.is_valid():
            data = form_login.cleaned_data
            user = authenticate(username=data['trainer_name'], password=data['password'])  
            if user is not None:
                if isinstance(user, User): 
                    login(request, user)
                    return render(request, 'trainers/login_thanks.html')
                else:
                    messages.error(request, 'Invalid trainer credentials') 
        else:
            messages.error(request, 'Invalid username or password') 
    else:
        form_login = TrainerLoginForm() 
    context = {"form_login": form_login}
    return render(request, 'trainers/trainer_login.html', context=context)  
#................................................
#................................................................
def LogoutTrainer(request):
    logout(request)
    return redirect('trainers:trainer_login') 
#......................................
# def change_password(request):
#     if request.method == 'POST':
#         form = CustomPasswordChangeForm(data=request.POST, user=request.user)
#     else:
#         form = CustomPasswordChangeForm(user=request.user)

#     context = {'form': form}  
#     return render(request, 'trainers/password_change.html', context=context)
def change_password(request):
    if not request.user.is_authenticated:
        return render(request, 'errors/please_login.html', status=403)

    if request.method == 'POST':
        form = CustomPasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return render(request, 'status/change_suc.html')
    else:
        form = CustomPasswordChangeForm(user=request.user)

    context = {'form': form}
    return render(request, 'trainers/password_change.html', context)