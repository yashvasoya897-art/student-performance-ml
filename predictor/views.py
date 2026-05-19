from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .models import PredictionHistory, Profile

import numpy as np
import joblib
import json
import os
from django.conf import settings


# =========================
# LOAD MODEL ONCE (IMPORTANT FIX)
# =========================
model_path = os.path.join(settings.BASE_DIR, "model.pkl")
model = joblib.load(model_path)


# =========================
# HOME / PREDICTION VIEW
# =========================
@login_required(login_url="/")
def home(request):

    result = None
    feedback = None

    if request.method == "POST":

        try:
            hours = float(request.POST.get("study_hours"))
            attendance = float(request.POST.get("attendance"))
            sleep = float(request.POST.get("sleep_hours"))
            prev_marks = float(request.POST.get("prev_marks"))

            # ML INPUT
            input_data = np.array([[hours, attendance, sleep, prev_marks]])

            prediction = model.predict(input_data)
            result = round(float(prediction[0]), 2)

            # FEEDBACK SYSTEM
            if result >= 80:
                feedback = "Excellent performance 🔥"
            elif result >= 60:
                feedback = "Good, keep improving 👍"
            elif result >= 40:
                feedback = "Average performance ⚠️"
            else:
                feedback = "Needs improvement 📉"

            # SAVE HISTORY
            PredictionHistory.objects.create(
                user=request.user,
                hours=hours,
                result=result
            )

        except Exception as e:
            result = None
            feedback = f"Error: {str(e)}"

    return render(request, "home.html", {
        "result": result,
        "feedback": feedback
    })


# =========================
# LOGIN
# =========================
def login_view(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid Username or Password")

    return render(request, "login.html")


# =========================
# LOGOUT
# =========================
def logout_view(request):
    logout(request)
    return redirect("login")


# =========================
# REGISTER
# =========================
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


# =========================
# DASHBOARD
# =========================
@login_required(login_url="/")
def dashboard(request):

    data = PredictionHistory.objects.filter(user=request.user)
    total = data.count()

    if total == 0:
        return render(request, "dashboard.html", {"total": 0})

    results = [i.result for i in data]

    return render(request, "dashboard.html", {
        "total": total,
        "avg": sum(results) / total,
        "max": max(results),
        "min": min(results),
    })


# =========================
# HISTORY
# =========================
@login_required(login_url="/")
def history_view(request):

    data = PredictionHistory.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(request, "history.html", {
        "data": data
    })


# =========================
# GRAPH
# =========================
@login_required(login_url="/")
def graph_view(request):

    data = PredictionHistory.objects.filter(user=request.user)

    hours = [i.hours for i in data]
    results = [i.result for i in data]

    return render(request, "graph.html", {
        "hours": json.dumps(hours),
        "results": json.dumps(results),
    })


# =========================
# PROFILE
# =========================
@login_required(login_url="/")
def profile_view(request):

    profile, created = Profile.objects.get_or_create(user=request.user)

    total_predictions = PredictionHistory.objects.filter(
        user=request.user
    ).count()

    return render(request, "profile.html", {
        "profile": profile,
        "total_predictions": total_predictions,
    })


# =========================
# SITEMAP
# =========================
def sitemap_xml(request):

    xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://student-performance-ml-jiy7.onrender.com/</loc>
    </url>
    <url>
        <loc>https://student-performance-ml-jiy7.onrender.com/register/</loc>
    </url>
    <url>
        <loc>https://student-performance-ml-jiy7.onrender.com/home/</loc>
    </url>
</urlset>"""

    return HttpResponse(xml, content_type="text/xml")
