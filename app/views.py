from django.shortcuts import render , redirect , HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login

from Comunication_LTD.settings import BASE_DIR
from .form import LoginForm , RegisterForm , CustomerForm , SearchForm , ForgetPasswordForm , SettingForm , SettingAdminForm
from django.db import connection
from django.contrib.auth.hashers import make_password
from .models import User
from .password import CheckPasswordIsOk ,sendEmailVerifiction
import ast
import datetime
import json


#Action For Register Method
def Register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            print("Trying Register...")
            lastname = form.cleaned_data['lastname']
            firstname = form.cleaned_data['firstname']
            birthday = form.cleaned_data['birthday']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirmpassword = form.cleaned_data['confirmpassword']
            try:
                # Check if Costumer is all ready exist
                SqlQuery = """SELECT email FROM app_user WHERE email = %s"""
                with connection.cursor() as cursor:
                    cursor.execute(SqlQuery, [email])
                    results = cursor.fetchall()
                    if len(results) == 1:
                        raise Exception("This User is all ready exist")
                
                checkPassword = CheckPasswordIsOk(password)
                if checkPassword is not None:
                    raise Exception(checkPassword)
                
                # Define the SQL INSERT statement
                current_datetime = datetime.datetime.now()
                date_join = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
                birthday = birthday.strftime('%Y-%m-%d %H:%M:%S')
                hashed_password = make_password(password, salt=None, hasher='pbkdf2_sha256') #Its make Random salt

                SqlQuery = """INSERT INTO app_user (firstname, lastname, birthday, email, password , is_superuser , is_active ,is_staff ,date_joined) 
                        VALUES (%s, %s, %s, %s, %s , %s ,%s , %s , %s)"""
                # Define the values to insert
                values = (firstname, lastname, birthday , email, hashed_password, False , True , False , date_join)

                # Execute the SQL statement
                with connection.cursor() as cursor:
                    cursor.execute(SqlQuery, values)
                print("""Add New User \n----------------------""")
                return HttpResponseRedirect('/login')  # Redirect to the same page after successful addition
            except Exception as error:
                # Handle other exceptions
                print(f"""   An error occurred: {error} \n-------------------""")
                messages.error(request,error)
                context = {'form' : form ,  'Error' : error}
                return render(request, 'user.html', context) # Redirect to the same page after error           
        else:
            error = "Your Values in InValid"
            print(f"{error}\n---------")
            context = {'form' : form , 'Error' : error}
            return render(request, 'user.html', context)                      
    elif request.Method == "GET":
        form = RegisterForm()
        context = {'form' : form ,'Error' : None}
        print("Building Empty Register Form..")
        return render(request, 'user.html', context)
    else:
         return render(request, '404.html')


#Action For login Method
def Login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        path = BASE_DIR/'static'/'config.txt'
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
                print(user.id)
                request.session['user_id'] = user.id
                print(User.objects.get(id=user.id).firstname)
                
                request.session['user_name'] = User.objects.get(id=user.id).firstname
                request.session['user_IsAdmin'] = User.objects.get(id=user.id).is_superuser
                request.session['login_attempts'] = 0
                
                messages.success(request, 'Successfully logged in!')
                return HttpResponseRedirect('/Communication_LTD/Add_Customer')  # Redirect to a success page.
            else:
                request.session.setdefault('login_attempts', 0)
                request.session['login_attempts'] += 1   
                try:
                    with open(path, 'r+') as file:
                    # Read the entire contents of the file
                        config_text = file.read()
                        initialdata = json.loads(config_text)
                        file.close()
                        
                    if(request.session['login_attempts'] >= initialdata['attempt']):
                        SqlQuery = "UPDATE app_user SET is_active = False WHERE email = %s"
                        with connection.cursor() as cursor:
                            cursor.execute(SqlQuery , [email])
                        request.session['login_attempts'] = 0
                        raise Exception("You over you attempts - user is lock")

                    error = "   Invalid Email or password."
                    context = {'form' : form , 'Type' : 'Login' , 'Error' : error}
                    return render(request, 'user.html', context)
                except Exception as error:
                    context = {'form' : form , 'Type' : 'Login' , 'Error' : error}
                    return render(request, 'user.html', context)
              
    elif request.method == "GET":
        form = LoginForm()
        context = {'form' : form , 'Type' : 'Login' , 'Error' : None}
        print("------------\nBuilding Login form..\n--------")
        return render(request , "user.html" , context)
    else:
        return render(request , "404.html")


#Action For Communication_LTD Method
def Search(request):
    if request.session.get('user_id'):
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
                context = {'form' : form , 'Type' : 'User', 'results' : results ,'name': request.session['user_name']}
                return render(request, 'search.html', context)

            except Exception as error:
                # Handle other exceptions
                print(f"""   An error occurred: {error} \n-------------------""")
                context = {'form' : form , 'Type' : 'User', "Error" : error}
                messages.error(request,error)
                return render(request, 'search.html', context) # Redirect to the same page after error   
        else:
            form = SearchForm()
            context = {'form' : form , 'Type' : 'User' ,'Error' : None , 'results' : None , 'name': request.session['user_name']}
            print("Building Communication_LTD Page..")
            return render(request, 'search.html', context)
    else:
        return render(request, '404.html')


def Add_Customer(request):
    if request.session.get('user_id'):
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
                    print("Add New Customer \n----------------------")
                    context = {'form' : form , 'Type' : 'User' , "Error" : None , 'message_success': "Add New Customer" }
                    return render(request, 'user.html', context)
                    #return HttpResponseRedirect('/Communication_LTD/Add_Customer')  # Redirect to the same page after successful addition
            
                except Exception as error:
                    # Handle other exceptions
                    print(f"""   An error occurred: {error} \n-------------------""")
                    context = {'form' : form , 'Type' : 'User' , 'Error' : error}
                    messages.error(request,error)
                    return render(request, 'user.html', context) # Redirect to the same page after error           
            else:
                print("   Your Values in InValid\n------------")
                error = "Your Values in InValid"
                context = {'form' : form , 'Type' : 'User' , "Error" : error}
                return render(request, 'user.html', context)
        else:
            form = CustomerForm()
            context = {'form' : form , 'Type' : 'User' , 'Error' : None, 'message_success': None,  'name': request.session['user_name']}
            print("Building Communication_LTD/Add Page..")
            return render(request, 'user.html', context)
    else:
        return render(request, '404.html')
    
def Setting(request):
    path = BASE_DIR/'static'/'config.txt'
    if request.session.get('user_id'):
        if request.method == 'POST':
            form = None
            if request.session['user_IsAdmin']:
                print("------------------\n    Setting Admin...")
                form = SettingAdminForm(request.POST)
            else:
                print("------------------\n    Setting User...")
                form = SettingForm(request.POST)

            if form.is_valid():
                #Cleaning Data After do Action
                password = form.cleaned_data['password']
                lenght_min = form.cleaned_data['lenght_min']
                lenght_max = form.cleaned_data['lenght_max']
                contain = ast.literal_eval(form.cleaned_data['contain']) # -->convert to list
                attempt = form.cleaned_data['attempt']
                forbidden = ast.literal_eval(form.cleaned_data['forbidden']) # -->convert to list
                history = form.cleaned_data['history']
            
                try:
                    checkPassword = CheckPasswordIsOk(password)
                    if checkPassword is not None:
                        raise Exception(checkPassword)
                    
                    hashed_password = make_password(password, salt=None, hasher='pbkdf2_sha256') #Its make Random salt
                    config_info = {"lenght_min": lenght_min ,"lenght_max": lenght_max , "contain": contain ,"attempt": attempt ,"forbidden": forbidden, "history": history }
                    userId = request.session["user_id"]


                    with open(path , "w") as file:
                        upadted_config = json.dumps(config_info, indent=4) #indent => 4 spaces ' ' - more readable
                        file.write(upadted_config)
                        file.close()
                        
                    # Check if Costumer is all ready exist
                    print(" Trying to upadte the info")
                    SqlQuery = "UPDATE app_user SET password = %s WHERE id = %s"
                    with connection.cursor() as cursor:
                        cursor.execute(SqlQuery, [hashed_password, userId])
                        
                    print(" Succseful upadte\n----------")
                    messages.success(request, "Succseful upadted setting of user")
                    context = {'form' : form , 'Type' : 'User' , "Error" : None ,'message_success': 'Succseful upadte' ,'name': request.session['user_name'] }
                    return render(request, 'setting.html', context)

                except Exception as error:
                    # Handle other exceptions
                    print(f"""   An error occurred: {error} \n-------------------""")
                    messages.error(request,error)
                    context = {'form' : form , 'Type' : 'User' , 'Error' : error}
                    return render(request, 'setting.html', context) # Redirect to the same page after error   
            else:
                error = "Your Values in InValid"
                context = {'form' : form , 'Type' : 'User' , 'name': request.session['user_name'] , 'Error' : error}
                print("Building Setting Page..\n---------")
                return render(request, 'setting.html', context)
        else:
            if request.session['user_IsAdmin']:
                with open(path, 'r+') as file:
                    # Read the entire contents of the file
                    config_text = file.read()
                    initialdata = json.loads(config_text)
                    print(initialdata)
                    file.close()
                form = SettingAdminForm(initial=initialdata)
            else:
                form = SettingForm()
            context = {'form' : form , 'Type' : 'User' , 'Error' : None, 'message_success': None ,'name': request.session['user_name']}
            print("Building Setting Page..")
            return render(request, 'setting.html', context)
    else:
        return render(request, '404.html')



def ForgetPassword(request):
    if request.method == 'POST':
        form = ForgetPasswordForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            code = form.cleaned_data['code']
            
            try:
                if(request.session["code"] != None):
                    print(request.session["code"])
                    print(code)
                    if str(request.session["code"]) != str(code):
                        raise Exception("Your Code Is not Correct")
                    
                    checkPassword = CheckPasswordIsOk(password)
                    if checkPassword is not None:
                        raise Exception(checkPassword)
                    
                    hashed_password = make_password(password, salt=None, hasher='pbkdf2_sha256') #Its make Random salt

            
                    print(" Trying to upadte the info")
                    SqlQuery = "UPDATE app_user SET password = %s WHERE email = %s"
                    with connection.cursor() as cursor:
                        cursor.execute(SqlQuery, [hashed_password, email])
                        
                    print(" Succseful upadte\n----------")
                    request.session.flush()
                    messages.success(request, "Succseful upadted setting of user")
                    context = {'form' : None , 'Type' : "Login" , "Error" : None ,'message_success': 'New Password' }
                    return render(request, 'user.html', context)
                else:
                    print("Sending to your mail code..")
                    code = sendEmailVerifiction(email)
                    request.session["code"] = code
                    context = {'form' : form , 'Type' : "Code" , 'Error' : None, 'message_success': None }
                    print("Building ForgetPassword Page..")
                    return render(request, 'forgetpassword.html', context)
            except Exception as error:
                context = {'form' : form , 'Type' : "Code" , 'Error' : error, 'message_success': None}
                print("Building ForgetPassword Page..")
                return render(request, 'forgetpassword.html', context)
        else:   
            context = {'form' : form , 'Type' : "Code" , 'Error' : None, 'message_success': None}
            return render(request, 'forgetpassword.html', context)   
    else:
        form = ForgetPasswordForm()
        request.session["code"] = None
        context = {'form' : form , 'Type' : None , 'Error' : None, 'message_success': None}
        print("Building ForgetPassword Page..")
        return render(request, 'forgetpassword.html', context)


def Logout(request):
    request.session.flush()
    return HttpResponseRedirect("/login")

#Action For Communication_LTD Method
def Hello_World():
     return HttpResponse("Hello World")
 
def view_404(request):
     return render(request, '404.html')
 
