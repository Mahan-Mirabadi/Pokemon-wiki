from django.shortcuts import render,redirect

# Create your views here.
def ViewHome(request):
    return render(request,'home/home.html')
def About(request):
    return render(request,'home/about.html')
def redirect_home (request):
    return redirect('home:view_home')