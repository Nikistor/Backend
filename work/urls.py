"""
URL configuration for work project.

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

from vacancies import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Список городов (Фильтрация)
    path('', views.GetCities, name='cities'),
    # Сведения о городе
    path('city/<int:id>/', views.GetCity, name='url_city'),
    # Фильтрация
    # path('filter/', views.Filter, name='filter'),
    # Удаление города
    path('delete_city/', views.DeleteCityByID, name='delete_city'),
]
