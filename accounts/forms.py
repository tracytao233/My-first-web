from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *

class HomeworkForm(ModelForm):
	class Meta:
		model = Homework
		fields = ['name', 'category', 'description','deadline']

class ProgressForm(ModelForm):
	class Meta:
		model = Progress
		fields = '__all__'


class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']


class StudentForm(ModelForm):
	class Meta:
		model = Student
		fields = '__all__'
		exclude = ['user']