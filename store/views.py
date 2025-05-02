from django.shortcuts import render, redirect
from .models import  *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import   UserCreationForm
from .forms import SignUpForm


def category(request, foo):
    #replace hyphens with space
    foo = foo.replace('-', '')
    #grap the category from url 
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products,'category':category})
    except:
        messages.success(request, ("hey category doesnt exist"))
        return redirect('home')


def product(request, pk):
    product =Product.objects.get(id= pk)
    return render(request, "product.html", {'product':product})

def home (request):
    products = Product.objects.all()
    return render(request, 'home.html',{'products':products})

def about  (request):
    return render(request, 'about.html')

def login_user (request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You  have been logged in"))
            return redirect('home')
        else:
            messages.success(request, ("There has been an error"))
            return redirect('login')

    else:
        return render (request, 'login.html', {})

def logout_user(request):

    logout(request)
    messages.success(request, ("You have been logged out"))
    return redirect('home')


def register_user(request):
    form = SignUpForm
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            #log in 
            login(request, user )
            messages.success(request, ("You have been registered successfully out"))
            return redirect('login')
        else:
            messages.success(request, ("There was a problem registering!"))
            return redirect ('register')
        
    else:    
        return render(request, 'register.html', {'form':form})



