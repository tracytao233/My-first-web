from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Student(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.name


class Tag(models.Model):
	name = models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.name

class Homework(models.Model):
	CATEGORY = (
			('Math', 'Math'),
			('English', 'English'),
            ('Chinese', 'Chinese'),
            ('French', 'French'),
            ('Economics','Economics'),
            ('Physics','Physics'),
            ('Chemistry','Chemistry'),
            ('Music', 'Music'),
            ('Psychology', 'Psychology'),
            ('Computer Science', 'Computer Science'),
			) 

	name = models.CharField(max_length=200, null=True)
	category = models.CharField(max_length=200, null=True, choices=CATEGORY)
	description = models.TextField(null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	deadline = models.DateTimeField(null=True, blank=True)
	tags = models.ManyToManyField(Tag)

	def __str__(self):
		return self.name


class Progress(models.Model):
	STATUS = (
			('Pending', 'Pending'),
			('Finished', 'Finished'),
			)
	student = models.ForeignKey(Student, null=True, on_delete= models.SET_NULL)
	homework = models.ForeignKey(Homework, null=True, on_delete= models.SET_NULL)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	status = models.CharField(max_length=200, null=True, choices=STATUS)
	
	def __str__(self):
		return self.status