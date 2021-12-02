from django.shortcuts import render, get_object_or_404, redirect
import requests

# Create your views here.
from WeatherApp.forms import CityForm
from WeatherApp.models import City


def CityWeatherView(request):

    url="http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=d83fcf82a77b7a5391a9cb186d0b46ae"
    errmsg = ''
    msg = ''
    msgclass = ''
    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            city_count = City.objects.filter(name=new_city).count()
            if city_count==0:
                r = requests.get(url.format(new_city)).json()
                print(r)
                if r['cod']==200:
                    form.save()
                else:
                    errmsg = "The City is not available in the world"
            else:
                errmsg = "Already City is added to database"
        if errmsg:
            msg = errmsg
            msgclass = 'is-danger'
        else:
            msg = "The City is successfully added in database"
            msgclass = 'is-success'

    form = CityForm()
    weather = []
    cities = City.objects.all()

    for city in cities:
        r = requests.get(url.format(city)).json()

        city_weather = {
            'city':city,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon':r['weather'][0]['icon'],
        }
        weather.append(city_weather)

    context = {
        'weathers':weather,
        'form':form,
        'msg':msg,
        'msgclass':msgclass,
    }
    return render(request, 'weather.html', context)


def City_delete(request, city_name):
    city=get_object_or_404(City, name=city_name)
    city.delete()
    return redirect('WeatherApp:city_weather')