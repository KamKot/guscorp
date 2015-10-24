# coding=utf-8
from django.shortcuts import render
from pererabotka.models import pererabotka, start, brigada
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, redirect
from django.core.paginator import Paginator
from django.contrib import auth
from pererabotka.forms import PerForm
from . import models
import datetime

# Create your views here.


def get_per(request, page_number=1):
    args = {}
    args.update(csrf(request))
    all_pererabotki = pererabotka.objects.all()
    current_page = Paginator(all_pererabotki, 1)
    args['pererabotki'] = current_page.page(page_number)
    args['username'] = auth.get_user(request).username
    args['form'] = PerForm
    return render_to_response('pererabotka.html', args)

# вывод стартовой страницы
def get_start(request):
    args = {}
    args.update(csrf(request))
    start_t = start.objects.all()
    args['start_txt'] = start_t
    args['username'] = auth.get_user(request).username
    return render_to_response('start.html', args)

# добавление переработок в базу
def add_per(request):
    if request.method == 'POST':
        b = models.brigada(name=request.POST['name'])
        a = models.pererabotka(p_id=request.POST['p_id'], p_date_start=request.POST['date_start'],
                               p_time_start=request.POST['time_start'], p_date_finish=request.POST['date_finish'],
                               p_time_finish=request.POST['time_finish'], p_address=request.POST['address'],
                               p_description=request.POST['description'], hours_cost=request.POST['p_hours_cost'])

        chasy = {'00:30': 0.5, '01:00': 1, '01:30': 1.5, '02:00': 2, '02:30': 2.5, '03:00': 3, '03:30': 3.5, '04:00': 4,
                 '04:30': 4.5, '05:00': 5, '05:30': 5.5, '06:00': 6, '06:30': 6.5, '07:00': 7, '07:30': 7.5, '08:00': 8,
                 '08:30': 8.5, '09:00': 9, '09:30': 9.5, '10:00': 10, '10:30': 10.5, '11:00': 11, '11:30': 11.5,
                 '12:00': 12, '12:30': 12.5, '13:00': 13, '13:30': 13.5, '14:00': 14, '14:30': 14.5, '15:00': 15,
                 '15:30': 15.5, '16:00': 16, '16:30': 16.5, '17:00': 17, '17:30': 17.5, '18:00': 18, '18:30': 18.5,
                 '19:00': 19, '19:30': 19.5, '20:00': 20, '20:30': 20.5, '21:00': 21, '21:30': 21.5, '22:00': 22,
                 '22:30': 22.5, '23:00': 23, '23:30': 23.5}

        noch_start = datetime.datetime.today().replace(hour=00, minute=00)
        noch_fin = datetime.datetime.today().replace(hour=6, minute=00)
        noch_start1 = datetime.datetime.today().replace(hour=22, minute=00)
        noch_fin1 = datetime.datetime.today().replace(hour=23, minute=59)

        date_s = datetime.datetime.strptime(a.p_date_start, '%Y-%m-%d')
        date_f = datetime.datetime.strptime(a.p_date_finish, '%Y-%m-%d')
        q = int(a.p_time_start[:2])  # часы
        w = int(a.p_time_start[3:5])  # минуты
        nachalo = datetime.datetime.today().replace(hour=q, minute=w)
        nachalo_x = (datetime.datetime.today().replace(hour=q, minute=w)).strftime('%H:%M')
        nachalo_x = chasy.get(nachalo_x)  # количество часов  и минут в числовом формате
        q = int(a.p_time_finish[:2])  # часы
        w = int(a.p_time_finish[3:5])  # минуты
        konec = datetime.datetime.today().replace(hour=q, minute=w)
        konec_x = datetime.datetime.today().replace(hour=q, minute=w).strftime('%H:%M')
        konec_x = chasy.get(konec_x)  # количество часов  и минут в числовом формате
        #stop_date = konec - datetime.timedelta(hours=3.5)

        if date_s == date_f:
            if noch_start <= nachalo <= noch_fin and noch_start1 <= konec <= noch_fin1:
                # Если  время начала переработок между 00 и 06 и конец между 22 и 23:59
                sum_chas = konec - datetime.timedelta(hours=nachalo_x)  # вычисляем общее количество отработанных часов
                noch_chas = (sum_chas - datetime.timedelta(hours=16)).strftime('%H:%M')  # приводим к строковому виду
                x = chasy.get(noch_chas)  # выбираем из словаря соответствие в числовом виде
                den = 16 * 1.5 * 173.5
                noch = x * 2 * 173.5
                a.total_sum = den + noch
            elif noch_start <= nachalo <= noch_fin and noch_fin < konec < noch_start1:
                # Если  время начала переработок между 00 и 06 и конец между 6 и 22:00
                sum_chas = konec - datetime.timedelta(hours=nachalo_x)
                noch_chas_x = noch_fin - datetime.timedelta(hours=nachalo_x)
                noch_chas = (noch_fin - datetime.timedelta(hours=nachalo_x)).strftime('%H:%M')
                x = chasy.get(noch_chas)
                den_chas = (sum_chas - datetime.timedelta(hours=x)).strftime('%H:%M')
                y = chasy.get(den_chas)
                den = y * 1.5 * 173.5
                noch = x * 2 * 173.5
                a.total_sum = den + noch
            elif noch_fin <= nachalo <= noch_start1 and noch_start1 < konec <= noch_fin1:
                # Если  время начала переработок после 6:00 и конец между 22 и 23:59
                sum_chas = konec - datetime.timedelta(hours=nachalo_x)
                noch_chas = (konec - datetime.timedelta(hours=22)).strftime('%H:%M')
                x = chasy.get(noch_chas)  # ночные часы
                den_chas = (sum_chas - datetime.timedelta(hours=x)).strftime('%H:%M')
                y = chasy.get(den_chas)  # дневные часы
                den = y * 1.5 * 173.5
                noch = x * 2 * 173.5
                a.total_sum = den + noch
            elif noch_fin <= nachalo < konec <= noch_start1:
                # Если  время начала переработок 06 и конец 22
                sum_chas = (konec - datetime.timedelta(hours=nachalo_x)).strftime('%H:%M')
                x = chasy.get(sum_chas)
                den = x * 1.5 * 173.5
                a.total_sum = den
            elif noch_start < nachalo < konec < noch_fin or noch_start1 < nachalo < konec < noch_fin1:
                # Если  время начала переработок между 00 и 06 или  между 22 и 23:59
                sum_chas = (konec - datetime.timedelta(hours=nachalo_x)).strftime('%H:%M')
                x = chasy.get(sum_chas)
                noch = x * 2 * 173.5
                a.total_sum = noch
        a.per_to_brigada_id = int(b.name[1])
        a.save()
    return redirect('/pererabotka/')
