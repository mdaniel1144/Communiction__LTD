from django import forms
from .models import Customer

class LoginForm(forms.Form):
    title = "Login"
    command = "Login"
    email = forms.CharField(label="Email", widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=100 , required=True)
    password = forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'class': 'form-control'}) , required=True)    
    
    
class RegisterForm(forms.Form):
    title = "Register"
    command = "Register"
    lastname = forms.CharField(label="Last Name", widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=100)
    firstname = forms.CharField(label="First Name", widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=100)
    birthday = forms.DateField(label="Birthday", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label="Email", widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=100)
    password = forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'class': 'form-control'}) , required=True)    
    confimpassword = forms.CharField(label="Confrim Password",widget=forms.PasswordInput(attrs={'class': 'form-control'}) , required=True)    

class CustomerForm(forms.Form):
    title = "Add New Customer"
    command = "Add New"
    CHOICES = [
        ('Manager', 'Manager'),
        ('Assistant', 'Assistant'),
        ('Department Manager', 'Department Manager'),
        ('CEO', 'CEO'),
        ('Counselor', 'Counselor'),
        ('Employee', 'Employee'),
    ]
    lastname = forms.CharField(label="Last Name:", widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=100)
    firstname = forms.CharField(label="First Name:", widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=100)
    birthday = forms.DateField(label="Birthday:", widget=forms.DateInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label="Phone Number:", widget=forms.TextInput(attrs={'class': 'form-control'}) ,max_length=100)
    email = forms.CharField(label="Email:", widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=100)
    city = forms.CharField(label="City:",widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=100)
    street = forms.CharField(label="Street:",widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=100)
    job = forms.ChoiceField(label="Job:", choices=CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    
    
class SearchForm(forms.Form):
    title = "Search by"
    command = "Search"
    CHOICES = [('Job', 'Job'), ('Email', 'Email'), ('City', 'City'),]
    type = forms.ChoiceField(label="Type:", choices=CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    text = forms.CharField(label="text",widget=forms.TextInput(attrs={'class': 'form-control'}))    
   