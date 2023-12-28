# views - обработчик приложения
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.shortcuts import render, redirect
from datetime import date

from .database import Database
from .models import City

# Вывод карточек с фильтрацией
def GetCities(request):
    filter_field = request.GET.get('filter_field')
    if filter_field is None:
        cities = City.objects.filter(status=True)
    else:
        cities = City.objects.filter(name=filter_field, status=True)
    # cities = City.objects.filter(status=True)
    return render(request, 'cities.html', {'data': {
        'current_date': date.today(),
        # 'cities': DB_get_city_with_status
        'cities': cities
    }})

# Вывод карточки по выбранному городу
def GetCity(request, id):
    city = City.objects.get(id=id)
    return render(request, 'city.html', {'data': {
        'current_date': date.today(),
        'city': city
    }})

# Фильтрация, поиск по названию города
# def Filter(request):
#     # filter_keyword = request.GET.get('filter_keyword')
#     filter_field = request.GET.get('filter_field')
#
#     if not filter_field:
#         return HttpResponseBadRequest("Необходимо указать ключевое слово и поле для фильтрации")
#
#     # if not filter_keyword or not filter_field:
#         # messages.error(request, 'Необходимо указать ключевое слово и поле для фильтрации')
#         # return redirect('filter')  # Ссылка на URL, на который мы хотим перенаправить пользователя
#
#     # Преобразовать ключевое слово в строку для поиска в базе данных
#     # filter_keyword = str(filter_keyword)
#     filter_field = str(filter_field)
#
#     # Получить список услуг из базы данных
#     # filtered_services = []
#     filtered_services = City.objects.filter(name=filter_field)
#
#     # DB = City.objects.all()
#     #
#     # database = []
#     # # Пройти по каждому объекту и создать словарь с необходимыми значениями
#     # for obj in DB:
#     #     data = {
#     #         'id': obj.id,
#     #         'name': obj.name,
#     #         'foundation_date': obj.foundation_date,
#     #         'GRP': obj.grp,
#     #         'climate': obj.climate,
#     #         'square': obj.square,
#     #         'description': obj.description,
#     #     }
#     #     database.append(data)
#     #
#     # filtered_services = [service for service in database if filter_field.lower() in service['name'].lower()]
#
#     return render(request, 'filters.html', {'database': filtered_services})

# Удаление карточки

# Удаление города по id
def DeleteCityByID(request):
    if request.method == 'POST':
        # Получаем значение city_id из POST-запроса
        city_id = int(request.POST.get('city_id'))
        if (city_id is not None):
            # Выполняем SQL запрос для редактирования статуса
            DB = Database()
            DB.connect()
            DB.update_status_delete_city(status=False, id_city=city_id)
            DB.close()
        # Перенаправим на предыдующую ссылку после успешного удаления
        return redirect('cities')
