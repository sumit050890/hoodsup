from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django import forms
from .forms import UserLoginForm, UserRegistrationForm, AWSInstanceForm


# Create your views here.
def signin(request):
    next = request.GET.get('next')
    # print(request.user.is_authenticated())
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect("/awssetup")

        # print(request.user.is_authenticated())

    return render(request, "login.html", {'form': form})


def register(request):
    # print(request.user.is_authenticated())
    next = request.GET.get('next')
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        if next:
            return redirect(next)
        return redirect("/awssetup")
    context = {"form": form}
    return render(request, 'register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect("/")


def aws_submit(request):
    next = request.GET.get('next')
    form = AWSInstanceForm(request.POST or None)
    print("user:" + request.user.username)
    if form.is_valid():
        userObj = form.cleaned_data
        print("aws-parameters:")
        print(userObj)

        # form.save()
        if next:
            return redirect(next)
        return redirect("/awssetup")
    return render(request, 'aws_setup.html', {'form': form})
