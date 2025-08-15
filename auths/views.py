from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from dashboard.models import AccountDetail
from .forms import Register
from django.db import IntegrityError


# Create your views here.


def login_user(request):
    logout(request)
    error = None
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")

        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect("dashboard")
        else:
            error = "Invalid username or password."
    return render(request, "login_form.html", {"error": error})


def register(request):
    form = Register()
    integrity_error = None
    if request.method == "POST":
        form = Register(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(
                    request, "Registration successful! You can now log in."
                )
                return redirect("login")
            except IntegrityError:
                integrity_error = "A user with that username or email already exists."
        # If not valid, errors will be shown in template
    context = {"form": form, "integrity_error": integrity_error}
    return render(request, "register.html", context)
