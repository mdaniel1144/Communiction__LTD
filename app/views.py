from django.shortcuts import render , redirect , HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .form import LoginForm , RegisterForm , CustomerForm , SearchForm
from django.db import connection
import datetime



#Action For Register Method
def Register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            print("Trying Register...")
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Successfully logged in!')
                return redirect('user.html')  # Redirect to a success page.
            else:
                context = {'form' : form , 'Type' : 'Register'}
                messages.error(request, 'Invalid username or password.')
                return render(request, 'user.html', context)
    else:
        form = RegisterForm()
        context = {'form' : form , 'Type' : 'Register'}
        print("Building Empty Register Form..")
        return render(request, 'user.html', context)


#Action For login Method
def Login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            print("---------------")
            print("Trying Login...")
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                print('       Successfully logged in!     ')
                print(f'       Wellcome  {email}         ')
                print(f'---------------------------------')
                messages.success(request, 'Successfully logged in!')
                return HttpResponseRedirect('/Communication_LTD/Add_Customer')  # Redirect to a success page.
            else:
                context = {'form' : form , 'Type' : 'Login'}
                print("'Invalid Email or password.")
                messages.error(request, 'Invalid Email or Password.')
                return render(request, 'user.html', context)
        else:
            context = {'form' : form , 'Type' : 'Login'}
            messages.error(request,"Your Values in InValid")
            print("   Your Values in InValid")
            return render(request, 'user.html', context)
    else:
        form = LoginForm()
        context = {'form' : form , 'Type' : 'Login'}
        print("Building Empty login form..")
        return render(request, 'user.html', context)


#Action For Communication_LTD Method
def Search(request):
    form = SearchForm(request.GET or None)
    print("------------------\n    Searching...")
    if form.is_valid():
        #Cleaning Data After do Action
        typeSearch = form.cleaned_data['type']
        text = form.cleaned_data['text']
        try:
            # Check if Costumer is all ready exist
            SqlQuery = f"SELECT firstname || ' ' || lastname AS fullname, email, city, job FROM app_customer WHERE {typeSearch} LIKE '%{text}%'"
            print(f"    Try Searching by {typeSearch} which contain {text}\n----------------")
            with connection.cursor() as cursor:
                cursor.execute(SqlQuery)
                results = cursor.fetchall()
            if len(results) < 1:
                raise Exception("No Found Nothing")
            context = {'form' : form , 'Type' : 'Customer', 'results' : results}
            return render(request, 'search.html', context)

        except Exception as error:
            # Handle other exceptions
            print(f"""   An error occurred: {error} \n-------------------""")
            context = {'form' : form , 'Type' : 'Customer'}
            messages.error(request,error)
            return render(request, 'search.html', context) # Redirect to the same page after error   
    else:
        form = SearchForm()
        context = {'form' : form , 'Type' : 'Customer' , 'results' : None}
        print("Building Communication_LTD Page..")
        return render(request, 'search.html', context)


def Add_Customer(request):
    context = {}
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        print("-----------------------\n   Trying Add New Costumers")
        if form.is_valid():
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            birthday = form.cleaned_data['birthday']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            city = form.cleaned_data['city']
            street = form.cleaned_data['street']
            job = form.cleaned_data['job']

            try:
                # Check if Costumer is all ready exist
                SqlQuery = """SELECT email FROM app_customer WHERE email = %s"""
                with connection.cursor() as cursor:
                    cursor.execute(SqlQuery, [email])
                    results = cursor.fetchall()
                    if len(results) == 1:
                        raise Exception("This Customer is all ready exist")
                
                # Define the SQL INSERT statement
                current_datetime = datetime.datetime.now()
                formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
                SqlQuery = """INSERT INTO app_customer (firstname, lastname, birthday, phone, email, city , street , job ,date_join) 
                        VALUES (%s, %s, %s, %s, %s, %s , %s , %s , %s)"""
                # Define the values to insert
                values = (firstname, lastname, birthday , phone, email, city , street , job , formatted_datetime)

                # Execute the SQL statement
                with connection.cursor() as cursor:
                    cursor.execute(SqlQuery, values)
                print("""Add New Customer \n----------------------""")
                return HttpResponseRedirect('/Communication_LTD/Add_Customer')  # Redirect to the same page after successful addition
            
            except Exception as error:
                # Handle other exceptions
                print(f"""   An error occurred: {error} \n-------------------""")
                context = {'form' : form , 'Type' : 'Customer'}
                messages.error(request,error)
                return render(request, 'user.html', context) # Redirect to the same page after error           
        else:
            error = Exception("Your Values in InValid")
            context = {'form' : form , 'Type' : 'Customer'}
            messages.error(request,error)
            print("   Your Values in InValid")
            return render(request, 'user.html', context)
    else:
        form = CustomerForm()
        context = {'form' : form , 'Type' : 'Customer'}
        print("Building Communication_LTD Page..")
        return render(request, 'user.html', context)


#Action For Communication_LTD Method
def Hello_World(request):
     return HttpResponse("Hello World")
 
def view_404(request):
     return render(request, '404.html')
