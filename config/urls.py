"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from config import settings as setting
from core.dashboard.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('clinic/', include('core.clinic.urls')),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('login/', include('core.login.urls')),
    path('reports/', include('core.reports.urls')),
    path('security/', include('core.security.urls')),
    path('user/', include('core.user.urls')),
    path('', include('core.homepage.urls')),
]

if setting.DEBUG:
    urlpatterns += static(setting.MEDIA_URL, document_root=setting.MEDIA_ROOT)
