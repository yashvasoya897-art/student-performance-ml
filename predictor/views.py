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
from .forms import ProfileImageForm


# =========================
# LOAD MODEL ONCE (IMPORTANT FIX)
# =========================
model_path = os.path.join(settings.BASE_DIR, "model.pkl")
model = joblib.load(model_path)


# =========================
# HOME / PREDICTION VIEW
# =========================
def home(request):

    return render(request, "home.html")


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

        # password check
        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        # username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        # email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("register")

        # create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        # create profile only once
        Profile.objects.get_or_create(user=user)

        login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        messages.success(request, "Account created successfully")

        return redirect("home")

    return render(request, "register.html")

def signup_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # IMPORTANT LINE
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        messages.success(request, "Account created successfully")
        return redirect('home')

    return render(request, 'signup.html')
# =========================
# DASHBOARD
# =========================
@login_required(login_url="/")
def dashboard(request):

    result = None
    feedback = None

    # DASHBOARD STATS
    data = PredictionHistory.objects.filter(
        user=request.user
    )

    total = data.count()

    if total > 0:

        results = [i.result for i in data]

        avg = round(sum(results) / total, 2)
        highest = max(results)

    else:

        avg = 0
        highest = 0

    # PREDICTION SYSTEM
    if request.method == "POST":

        hours = float(request.POST.get("study_hours"))
        attendance = float(request.POST.get("attendance"))
        sleep = float(request.POST.get("sleep_hours"))
        prev_marks = float(request.POST.get("prev_marks"))

        input_data = np.array([
            [hours, attendance, sleep, prev_marks]
        ])

        prediction = model.predict(input_data)

        result = round(float(prediction[0]), 2)

        # SAVE HISTORY
        PredictionHistory.objects.create(
            user=request.user,
            hours=hours,
            result=result
        )

        # AI FEEDBACK
        import random

        excellent = [
            "🔥 Excellent consistency in academics.",
            "🚀 Outstanding predicted performance.",
            "🎯 Great work! Keep maintaining your routine."
        ]

        good = [
            "👍 Good progress, stay consistent.",
            "📚 You're doing well, improve gradually.",
            "💡 Nice performance, keep practicing daily."
        ]

        average = [
            "⚠️ Focus more on study routine.",
            "📖 Increase study hours for better marks.",
            "🧠 Practice revision regularly."
        ]

        low = [
            "🚨 Attendance and study routine need improvement.",
            "📉 Work on consistency and sleep schedule.",
            "💪 Start improving basics step by step."
        ]

        if result >= 80:
            feedback = random.choice(excellent)

        elif result >= 60:
            feedback = random.choice(good)

        elif result >= 40:
            feedback = random.choice(average)

        else:
            feedback = random.choice(low)

    return render(request, "dashboard.html", {

        "result": result,
        "feedback": feedback,

        "total": total,
        "avg": avg,
        "max": highest,

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

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        form = ProfileImageForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            form.save()

    else:

        form = ProfileImageForm(
            instance=profile
        )

    total_predictions = PredictionHistory.objects.filter(
        user=request.user
    ).count()

    return render(request, "profile.html", {

        "profile": profile,
        "form": form,
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
