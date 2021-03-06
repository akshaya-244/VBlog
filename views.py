from django.shortcuts import render,redirect
from django.contrib import messages,auth
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        #Get Form Values
        first_name= request.POST['first_name']
        last_name= request.POST['last_name']
        username= request.POST['username']
        email= request.POST['email']
        password= request.POST['password']
        password2=request.POST['password2']

        #Check if passwords match
        if password == password2:
            #Check username
            if User.objects.filter(username=username).exists():
                messages.error(request,'Username is taken')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request,'Email is taken')
                    return redirect('register')
                else:
                    #Looks good
                    user=User.objects.create_user(username=username,password=password,email=email,first_name=first_name,last_name=last_name)
                    #Login after registering
                    user.save()
                    messages.success(request,'You have registered successfully and can now log in!')
                    return redirect('login')
        else:
            #messages
            messages.error(request, 'Password do not match')
            return redirect('register')

    else:
        return render(request, 'accounts/register.html')

def logout(request):
    return redirect('home')

def dashboard(request):
    return render(request, 'accounts/dashboard.html')

def login(request):
    if request.method == 'POST':
        username= request.POST['username']
        password= request.POST['password']
        #Check username and password
        user=auth.authenticate(username=username, password=password)
        #if user is found in the database
        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are now logged in!")
            return redirect('dashboard')
        else:
            messages.error(request,'Invalid credentials')
            return redirect('login')
        #Login
       
    else:
        return render(request, 'accounts/login.html')

