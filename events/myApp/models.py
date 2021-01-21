from django.db import models

# Create your models here.
class User(models.Model):
    email=models.CharField(max_length=50,primary_key=True)
    password=models.CharField(max_length=50)
   

class Event(models.Model):
    title=models.CharField(max_length=50,primary_key=True)
    description=models.TextField(default=' ')
    date=models.DateField()
    creator=models.ForeignKey(User, on_delete=models.CASCADE)
   

class Participation(models.Model):
    participant=models.ForeignKey(User, on_delete=models.CASCADE)
    event=models.ForeignKey(Event, on_delete=models.CASCADE)