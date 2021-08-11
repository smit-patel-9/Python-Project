from django.db import models

# Create your models here.
class Submit(models.Model):
	name=models.CharField(max_length=50)
	email=models.CharField(max_length=50)
	number=models.IntegerField()
	remarks=models.TextField()

	def __str__(self):
		return self.name

class User(models.Model):
	fname=models.CharField(max_length=64)
	lname=models.CharField(max_length=64)
	email=models.CharField(max_length=64)
	number=models.CharField(max_length=64)
	address=models.TextField()
	password=models.CharField(max_length=64)
	cpassword=models.CharField(max_length=64)
	image=models.ImageField(upload_to="user_image/",default="")

	def __str__(self):
		return self.fname+ " " +self.lname 