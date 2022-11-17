from unicodedata import category
from django.db import models

# Create your models here.
class images_uploader(models.Model):
    images = models.ImageField(upload_to='static/Up_img')
    unique_token = models.CharField(max_length=80,blank=True)
    category = models.CharField(max_length=80,blank=True)
    family_name = models.CharField(max_length=80,blank=True)

    def __str__(self):
        return str(self.images)+str(self.unique_token)+str(self.category)+str(self.family_name)

class Sliced_image(models.Model):
    Unique_Token = models.CharField(max_length=80,blank=True)
    Family_name = models.CharField(max_length=80,blank=True)
    Images = models.ImageField(upload_to='static/Sliced')

    def __str__(self):
        return str(self.Family_name)+""+str(self.Images)+''+str(self.Unique_Token)

class User_Ceren(models.Model):
    Name = models.CharField(max_length=80,blank=True)
    Email = models.EmailField(max_length=80,blank=True)
    Password = models.CharField(max_length=250,blank=True)

    def __str__(self):
        return str(self.Name)+str(self.Email)


