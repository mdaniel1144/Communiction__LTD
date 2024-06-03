"""
URL configuration for Comunication_LTD project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Login , name="login"),
    path('login', views.Login , name="login"),
    path('logout', views.Logout , name="logout"),
    path('forget_password', views.ForgetPassword , name="forget_password"),
    path('register/', views.Register , name="register"),
    path('Communication_LTD/Search', views.Search , name="Search"),
    path('Communication_LTD/Add_Customer', views.Add_Customer , name="Add_Customer"),
    path('Communication_LTD/Setting', views.Setting , name="Setting"),

    
    #Check Server is Ok
    path('Hello_World', views.Hello_World , name="Hello_World"),
    path('404', views.view_404 , name="Add_Customer"),

]
