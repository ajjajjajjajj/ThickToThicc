"""AppStore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

from app.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('index', index, name='index'),
    # path('add', add, name='add'),
    # path('view/<str:id>', view, name='view'),
    # path('edit/<str:id>', edit, name='edit'),
    path('', home,name='home'),
    path('register', register_view, name='register'),
    path('registration_request', register_request, name='registration_request'),
    path('search', search_view),
    path('search_request', search_request, name='search_request'),
    path('login/',login_request,name='login'),
    path('<str:type>-<int:id>', logged_home, name = 'loggedhome'),
    path('recommends/<str:type>/', recommends_view, name='recommends'),
    path('rating',rating,name='rating'),
    path('browse',browse,name='browse')
]