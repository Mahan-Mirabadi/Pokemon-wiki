from django.db import models

# Create your models here.
class trainer(models.Model):
    name=models.CharField(max_length=30)
    lastname=models.CharField(max_length=30)
    email=models.EmailField(max_length=254)
    phone=models.CharField(max_length=100)
    adress=models.TextField()
    created_date=models.DateField(auto_now_add=True)