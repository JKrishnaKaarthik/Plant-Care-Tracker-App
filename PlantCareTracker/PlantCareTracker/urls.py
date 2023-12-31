"""
URL configuration for PlantCareTracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from signup.views import signup
from login.views import login, add_plant, get_plant_list, remove_plant
urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', signup),
    path('', login),
    path('add_plant/', add_plant),
    path('remove_plant/', remove_plant),
    path('get_plant_list/', get_plant_list),
]
