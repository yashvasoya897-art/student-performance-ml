"""
URL configuration for mlproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps.views import sitemap
from predictor import views


# =========================
# SITEMAP
# =========================
class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "daily"

    def items(self):
        return [
            "login",
            "register",
            "home",
        ]

    def location(self, item):
        return f"/{item}/" if item != "login" else "/"


sitemaps = {
    "static": StaticViewSitemap,
}


# =========================
# URL PATTERNS
# =========================
urlpatterns = [

    # Admin
    path('admin/', admin.site.urls),

    # Auth (ONLY ONE - KEEP SIMPLE)
    path('accounts/', include('django.contrib.auth.urls')),

    # Pages
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('home/', views.home, name='home'),

    # App pages
    path('dashboard/', views.dashboard, name='dashboard'),
    path('history/', views.history_view, name='history'),
    path('graph/', views.graph_view, name='graph'),
    path('profile/', views.profile_view, name='profile'),

    # Prediction (FIXED)
    path('predict/', views.home, name='predict'),

    # Logout
    path('logout/', views.logout_view, name='logout'),

    # Sitemap
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]

# MEDIA FILES
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
