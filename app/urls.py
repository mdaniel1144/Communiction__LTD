from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('Communication_LTD/Search', views.Search , name="Search"),
    path('Communication_LTD/Add_Customer', views.Add_Customer , name="Add_Customer"),
    path('Communication_LTD/Setting', views.Setting , name="Setting"),
]