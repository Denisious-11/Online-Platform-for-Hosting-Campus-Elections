from django.db import models

# Create your models here.
class Requests(models.Model):
    S_id=models.IntegerField(primary_key=True)
    Username=models.CharField(max_length=255)
    Email=models.CharField(max_length=255)
    Password=models.CharField(max_length=255)
    user_type=models.CharField(max_length=255)
    Phone=models.CharField(max_length=255)

class Users(models.Model):
    S_id=models.IntegerField(primary_key=True)
    Username=models.CharField(max_length=255)
    Email=models.CharField(max_length=255)
    Password=models.CharField(max_length=255)
    user_type=models.CharField(max_length=255)
    Phone=models.CharField(max_length=255)
    
class Nomination(models.Model):
    n_id=models.IntegerField(primary_key=True)
    candidate_name=models.CharField(max_length=255)
    candidate_dob=models.CharField(max_length=255)
    candidate_email=models.CharField(max_length=255)
    candidate_phone=models.CharField(max_length=255)
    candidate_department=models.CharField(max_length=255)
    candidate_gender=models.CharField(max_length=255)
    candidate_address=models.CharField(max_length=255)
    statement_of_intent=models.CharField(max_length=255)
    candidate_image=models.CharField(max_length=255)
    status=models.CharField(max_length=255, default='Pending')

class Vote_Time(models.Model):
    t_id=models.IntegerField(primary_key=True)
    s_time=models.CharField(max_length=255)
    e_time=models.CharField(max_length=255)
    status=models.CharField(max_length=255,default='Pending')

class Vote(models.Model):
    v_id=models.IntegerField(primary_key=True)
    candidate_name=models.CharField(max_length=255)
    get_id=models.IntegerField()