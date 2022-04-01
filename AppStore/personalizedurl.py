from django.urls import path, include

urlpatters = [
    path('', views.loggedhome, name="loggedhome")
]