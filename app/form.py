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
    confirmpassword = forms.CharField(label="Confirm Password",widget=forms.PasswordInput(attrs={'class': 'form-control'}) , required=True)    

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
    
class ForgetPasswordForm(forms.Form):
    title = "Forget Password"
    command = "Save"
    email = forms.CharField(label="Email", widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=100 , required=True)
    password = forms.CharField(label="New Password",widget=forms.PasswordInput(attrs={'class': 'form-control'}) ,required=False) 
    code = forms.IntegerField(label="Code",widget=forms.NumberInput(attrs={'class': 'form-control'}) ,required=False)


class SettingForm(forms.Form):
    title = "Setting"
    command = "Save"
    password = forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'class': 'form-control'}))    
    confirmpassword = forms.CharField(label="Confirm password",widget=forms.PasswordInput(attrs={'class': 'form-control'}))    
    
class SettingAdminForm(SettingForm):
    lenght_min = forms.IntegerField(label="lenght_min",widget=forms.NumberInput(attrs={'class': 'form-control'}))
    lenght_max = forms.IntegerField(label="lenght_max",widget=forms.NumberInput(attrs={'class': 'form-control'}))
    contain= forms.CharField(label="contain",widget=forms.Textarea(attrs={'class': 'form-control'}))
    attempt= forms.IntegerField(label="attempt",widget=forms.NumberInput(attrs={'class': 'form-control'}))
    forbidden= forms.CharField(label="forbidden",widget=forms.Textarea(attrs={'class': 'form-control'}))
    history = forms.CharField(label="history",widget=forms.Textarea(attrs={'class': 'form-control'}))