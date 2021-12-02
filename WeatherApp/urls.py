from django.urls import path

from WeatherApp import views

app_name = "WeatherApp"

urlpatterns = [
    path('', views.CityWeatherView, name="city_weather"),
    path('remove/<city_name>/', views.City_delete, name="city_remove"),

]