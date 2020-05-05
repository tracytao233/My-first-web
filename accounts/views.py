from django.shortcuts import render, redirect
from django.http import HttpResponse 
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, admin_only, allowed_users
from .models import *
from .forms import *
from .filters import *

# Create your views here.

@login_required(login_url='login')
@admin_only
def home(request):
	progresses = Progress.objects.all()
	students = Student.objects.all()
	homeworks = Homework.objects.all()
	total_students = students.count()
	total_progresses = progresses.count()
	total_homeworks = homeworks.count()
	finished = progresses.filter(status='Finished').count()
	pending = progresses.filter(status='Pending').count()
	context = {
	'progresses':progresses, 
	'students':students,
	'total_students': total_students,
	'total_progresses':total_progresses,
	'total_homeworks': total_homeworks,
	'finished':finished,
	'pending':pending,
	}

	return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def homeworks(request):
	homeworks = Homework.objects.all()
	return render(request, 'accounts/homeworks.html', {'homeworks':homeworks})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def student(request, pk_test):
	student = Student.objects.get(id=pk_test)
	progresses = student.progress_set.all()
	progresses_pending = progresses.filter(status='Pending').count()
	myFilter = ProgressFilter(request.GET, queryset=progresses)
	progresses = myFilter.qs 
	context = {
	'student':student,
	'progresses':progresses,
	'progresses_pending':progresses_pending,
	'myFilter':myFilter,
	}

	return render(request, 'accounts/student.html',context)

@login_required(login_url='login')
def addProgress(request):
	form = ProgressForm()
	if request.method == 'POST':
		form = ProgressForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {
		'form': form
	}
	return render(request, 'accounts/progress_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def addStudent(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			return redirect('/')
		
	context = {
		'form':form,
	}
	return render(request, 'accounts/student_form.html', context)

@login_required(login_url='login')
def addHomework(request):
	form = HomeworkForm()
	if request.method == 'POST':
		form = HomeworkForm(request.POST)
		if form.is_valid():
			user = form.save()
			return redirect('/')
		
	context = {
		'form':form,
	}
	return render(request, 'accounts/homework_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateStudent(request, pk):
	student = Student.objects.get(id=pk)
	form = StudentForm(instance=student)

	if request.method == 'POST':
		form = StudentForm(request.POST, instance=student)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {
		'form':form
	}

	return render(request, 'accounts/student_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateProgress(request, pk):
	progress = Progress.objects.get(id=pk)
	form = ProgressForm(instance=progress)

	if request.method == 'POST':
		form = ProgressForm(request.POST, instance=progress)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {
		'form':form
	}

	return render(request, 'accounts/progress_form.html', context)

@login_required(login_url='login')
def deleteProgress(request, pk):
	progress = Progress.objects.get(id=pk)
	if request.method == "POST":
		progress.delete()
		return redirect('/')

	context = {'item':progress}
	return render(request, 'accounts/delete.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createProgress(request, pk):
	ProgressFormSet = inlineformset_factory(Student, Progress, fields=('homework', 'status'), extra=3 )
	student = Student.objects.get(id=pk)
	formset = ProgressFormSet(queryset=Progress.objects.none(),instance=student)
	if request.method == 'POST':
		form = ProgressForm(request.POST)
		formset = ProgressFormSet(request.POST, instance=student)
		if formset.is_valid():
			formset.save()
			return redirect('/')

	context = {'form':formset}
	return render(request, 'accounts/progress_form.html', context)

@unauthenticated_user
def registerPage(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, 'Account was created for ' + username)
			return redirect('login')
		

	context = {'form':form}
	return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'accounts/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def userPage(request):
	progresses = request.user.student.progress_set.all()

	total_progresses = progresses.count()
	finished = progresses.filter(status='Finished').count()
	pending = progresses.filter(status='Pending').count()

	print('PROGRESSES:', progresses)

	context = {
	'progresses':progresses, 
	'total_progresses':total_progresses,
	'finished':finished,
	'pending':pending
	}
	return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def accountSettings(request):
	student = request.user.student
	form = StudentForm(instance=student)

	if request.method == 'POST':
		form = StudentForm(request.POST, request.FILES,instance=student)
		if form.is_valid():
			form.save()


	context = {'form':form}
	return render(request, 'accounts/account_settings.html', context)

