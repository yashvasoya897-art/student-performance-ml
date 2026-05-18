from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import PredictionHistory, Profile

import json

import joblib
import numpy as np

from django.conf import settings
import os

# HOME PAGE
@login_required(login_url="/")
def home(request):

    result = None
    feedback = None

    model_path = os.path.join(settings.BASE_DIR, "model.pkl")
    model = joblib.load(model_path)

    if request.method == "POST":

        hours = float(request.POST.get("hours"))
        attendance = float(request.POST.get("attendance"))
        sleep = float(request.POST.get("sleep"))
        prev_marks = float(request.POST.get("prev_marks"))

        input_data = np.array([[hours, attendance, sleep, prev_marks]])

        prediction = model.predict(input_data)

        result = round(prediction[0], 2)

        # 🤖 AI FEEDBACK LOGIC
        if result >= 80:
            feedback = "Excellent performance 🔥"
        elif result >= 60:
            feedback = "Good, keep improving 👍"
        elif result >= 40:
            feedback = "Average performance ⚠️"
        else:
            feedback = "Needs improvement 📉"

        PredictionHistory.objects.create(
            user=request.user,
            hours=hours,
            result=result
        )

    return render(request, "home.html", {
        "result": result,
        "feedback": feedback
    })

# LOGIN

def login_view(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("home")

        else:

            messages.error(
                request,
                "Invalid Username or Password"
            )

    return render(request, "login.html")


def logout_view(request):

    logout(request)

    return redirect("login")


# REGISTER
def register_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:

            messages.error(request, "Passwords do not match")

            return redirect("register")

        if User.objects.filter(username=username).exists():

            messages.error(request, "Username already exists")

            return redirect("register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        Profile.objects.create(user=user)

        messages.success(request, "Account Created Successfully")

        return redirect("login")

    return render(request, "register.html")


# DASHBOARD
@login_required(login_url="/")
def dashboard(request):

    data = PredictionHistory.objects.filter(
        user=request.user
    )

    total = data.count()

    if total == 0:

        context = {
            "total": 0
        }

    else:

        results = [i.result for i in data]

        context = {
            "total": total,
            "avg": sum(results) / total,
            "max": max(results),
            "min": min(results),
        }

    return render(request, "dashboard.html", context)


# HISTORY
@login_required(login_url="/")
def history_view(request):

    data = PredictionHistory.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(request, "history.html", {
        "data": data
    })

        "total_predictions": total_predictions,
    })
