from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms


def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'store/category_summary.html', {'categories': categories})
def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'store/product.html', {'product': product})


def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})


def about(request):
    return render(request, 'store/about.html', {})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You Have been Logged in. Welcome"))
            return redirect('home')
        else:
            messages.warning(request, ("Your username/password is not correect please try again."))
            return redirect('login')

    else:
        return render(request, 'store/login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, ("You Have been logged out! ... Thanks"))
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You are Registered!"))
            return redirect('home')
        else:
            messages.warning(request, ("Something wrong. Please try again."))
    else:
        return render(request, 'store/register.html', {'form': form})


def category(request, foo):
    # replace hyphen with spaces
    foo = foo.replace('-', ' ')
    # Grab the Category from the url
    try:
        # Lookup the category
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'store/category.html', {'products': products, 'category': category})
    except:
        messages.warning(request, ("Hey this Category doesn't exist!"))
        return redirect('home')
