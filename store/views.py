from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django import forms
from django.db.models import Q


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
            return redirect('update_info')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
            return redirect('register')
    else:
        return render(request, 'store/register.html', {'form': form})


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, "Profile has been updated.")
            return redirect('home')
        return render(request, "store/update_users.html", {'user_form': user_form})
    else:
        messages.warning(request, "You should be logged in to update your profile")
        return redirect('login')


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


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        # Did they fill out the form
        if request.method == 'POST':
            # Do stuff
            form = ChangePasswordForm(current_user, request.POST)
            # Is the form valid
            if form.is_valid():
                form.save()
                messages.success(request, "Password successfully updated.")
                # login(request, current_user)
                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')

        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'store/update_password.html', {'form': form})
    else:
        messages.warning(request, "You are not logged in")
        redirect('login')


def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)

        if form.is_valid():
            form.save()

            messages.success(request, "Your info has been updated.")
            return redirect('home')
        return render(request, "store/update_info.html", {'form': form})
    else:
        messages.warning(request, "You should be logged in to update your profile")
        return redirect('login')


def search(request):
    # Determined if they fill out the form
    if request.method == "POST":
        searched = request.POST['searched']
        # Query the products database model
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        # Test for Null
        if not searched:
            messages.warning(request, "No products were found based on your search criteria.")
            return redirect("search")
        else:
            return render(request, 'store/search.html', {'searched': searched})
    else:
        return render(request, 'store/search.html', {})