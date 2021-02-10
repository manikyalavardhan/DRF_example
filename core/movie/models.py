from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
	username = models.CharField(max_length=100,primary_key=True)
	password = models.CharField(max_length=500)
	
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = []

class UserCollection(models.Model):
	user_id = models.ForeignKey(User,on_delete=models.CASCADE)
	c_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	title = models.CharField(max_length=200)
	description = models.TextField()
	movies = models.JSONField()

# class Movies(models.Model):
# 	collection_id = models.ForeignKey(UserCollection,on_delete=models.CASCADE)
# 	movies = models.JSONField()