from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login ,logout
from .models import CustomUser
from django.contrib import messages
from django.http import JsonResponse
def home(request):
    user = request.user
    if user.is_authenticated:
        if user.role =="student":
            return render(request,'student.html')
        elif user.role == 'warden':
            return render(request,'warden.html')
        elif user.role == 'security':
            return render(request,'security.html')
        else :
           return render(request, 'index.html')
    else:
      return render(request, 'index.html')

def signup(request):
    if request.method == "POST":
        username = request.POST['userName']
        firstname = request.POST['firstName']
        lastname = request.POST['lastName']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']
        user = CustomUser.objects.create(username=username, role=role, email=email)
        user.set_password(password)
        user.first_name = firstname
        user.last_name = lastname
        user.save()
        messages.success(request, 'Account created successfully. You can now log in.')
        return redirect('login')
    return render(request, 'signup.html')

def loginView(request):
    if request.method == "POST":
        user = authenticate(username=request.POST['userName'], password=request.POST['password'])
        if user is None :
            messages.error(request, 'Invalid username, password, or role.')
        else:
           if user.role == 'security':
            login(request, user)
            return render(request,'security.html')
           elif user.role =="student":
            login(request, user)
            return render(request,'student.html')
           else:
            login(request, user)
            return render(request,'warden.html')
    return render(request, 'login.html')

def logoutView(request):
   logout(request)
   return redirect('login')

