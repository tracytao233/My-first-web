from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),

    path('', views.home, name = "home"),
    path('user/', views.userPage, name="user-page"),
    path('homeworks/', views.homeworks, name="homeworks"),
    path('student/<str:pk_test>/', views.student,name="student"),
    path('account/', views.accountSettings, name="account"),

    path('add_progress/', views.addProgress, name="add_progress"),
    path('add_student/', views.addStudent, name="add_student"),
    path('add_homeowork/', views.addHomework, name="add_homework"),
    path('update_student/<str:pk>/', views.updateStudent, name="update_student"),
    path('create_progress/<str:pk>/', views.createProgress, name="create_progress"),
    path('update_progress/<str:pk>/', views.updateProgress, name="update_progress"),
    path('delete_progress/<str:pk>/', views.deleteProgress, name="delete_progress"),

    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
    name="reset_password"),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), 
    name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), 
    name="password_reset_confirm"),
    path('reset_password_complete/', 
    auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), 
    name="password_reset_complete"),
]
