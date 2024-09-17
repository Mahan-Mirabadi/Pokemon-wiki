from django.shortcuts import render

# Create your views here.
def ViewHome(request):
    return render(request,'home/home.html')
def About(request):
    return render(request,'home/about.html')