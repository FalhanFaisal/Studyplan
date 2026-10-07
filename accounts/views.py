from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import SignUpForm


def signup(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome to StudyPlan! Your account has been created successfully. 🎉")
            return redirect("dashboard")
        else:
            messages.error(request, "Please correct the errors below to create your account.")
    else:
        form = SignUpForm()

    return render(request, "accounts/signup.html", {"form": form})
