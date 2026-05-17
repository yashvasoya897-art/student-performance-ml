from django.urls import path
from . import views

urlpatterns = [

    path("", views.login_view, name="login"),

    path("home/", views.home, name="home"),

    path("dashboard/", views.dashboard, name="dashboard"),

    path("graph/", views.graph_view, name="graph"),

    path("history/", views.history_view, name="history"),

    path("profile/", views.profile_view, name="profile"),

    path("logout/", views.logout_view, name="logout"),

    path("register/", views.register_view, name="register"),

]
