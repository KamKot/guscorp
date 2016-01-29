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


# вывод переработок
def get_per(request, page_number=1):
    args = {}
    args.update(csrf(request))
    user = auth.get_user(request).username
    user_id = auth.get_user(request).id
    all_pererabotki = pererabotka.objects.filter(per_to_brigada=user_id)
    #current_page = Paginator(all_pererabotki, 1)
    #args['pererabotki'] = current_page.page(page_number)
    args['pererabotki'] = all_pererabotki
    args['username'] = user
    y = 0
    for x in all_pererabotki:
        y += x.total_sum
    args['tsum'] = y
    return render_to_response('show_pererabotka.html', args)


def get_per2(request, date_per='2015-12-19'):
    args = {}
    args.update(csrf(request))
    user = auth.get_user(request).username
    user_id = auth.get_user(request).id
    all_pererabotki = pererabotka.objects.filter(per_to_brigada=user_id)
    date_pererabotki = pererabotka.objects.filter(p_date_start=date_per)
    args['date_pererabotki'] = date_pererabotki
    args['username'] = user
    y = 0
    for x in all_pererabotki:
        y += x.total_sum
    args['tsum'] = y
    return render_to_response('show_pererabotka.html', args)


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
    args = {}
    args['username'] = auth.get_user(request).username
    args['form'] = PerForm
    args.update(csrf(request))
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

        noch_start = 0
        noch_fin = 6
        noch_start1 = 22
        noch_fin1 = 24

        date_s = datetime.datetime.strptime(a.p_date_start, '%Y-%m-%d')
        date_f = datetime.datetime.strptime(a.p_date_finish, '%Y-%m-%d')
        cena_chasa = float(a.hours_cost)
        nachalo = a.p_time_start
        nachalo = chasy.get(nachalo)  # количество часов  и минут в числовом формате
        konec = a.p_time_finish
        konec = chasy.get(konec)

        if date_s == date_f:
            if noch_start <= nachalo <= noch_fin and noch_start1 <= konec <= noch_fin1:
                # Если  время начала переработок между 00 и 06 и конец между 22 и 23:59
                noch_chas = (noch_fin - nachalo) + (konec - noch_start1)  # ночные часы
                den_chas = noch_start1 - noch_fin  # дневные часы
                sum_noch = noch_chas * 2 * cena_chasa  # сумма за дневные
                sum_den = den_chas * 1.5 * cena_chasa  # сумма за ночные
                summa = sum_den + sum_noch  # общая сумма
                total_chas = den_chas + noch_chas  # общее количество отработанных часов
                kol_den_chas = den_chas  # количество ночных часов
                kol_nosh_chas = noch_chas  # количество дневных часов
                a.kol_noch = kol_nosh_chas  # запись в БД
                a.kol_den = kol_den_chas
                a.total_hours = total_chas
                a.den = sum_den
                a.noch = sum_noch
                a.total_sum = summa
            elif noch_start <= nachalo <= noch_fin and noch_fin < konec < noch_start1:
                # Если  время начала переработок между 00 и 06 и конец между 6 и 22:00
                noch_chas = (noch_fin - nachalo)
                den_chas = konec - noch_fin
                sum_noch = noch_chas * 2 * cena_chasa
                sum_den = den_chas * 1.5 * cena_chasa
                summa = sum_den + sum_noch
                total_chas = den_chas + noch_chas
                kol_den_chas = den_chas
                kol_nosh_chas = noch_chas
                a.kol_noch = kol_nosh_chas
                a.kol_den = kol_den_chas
                a.total_hours = total_chas
                a.den = sum_den
                a.noch = sum_noch
                a.total_sum = summa
            elif noch_fin <= nachalo <= noch_start1 and noch_start1 < konec <= noch_fin1:
                # Если  время начала переработок после 6:00 и конец между 22 и 23:59
                noch_chas = konec - noch_start1
                den_chas = noch_start1 - nachalo
                sum_noch = noch_chas * 2 * cena_chasa
                sum_den = den_chas * 1.5 * cena_chasa
                summa = sum_den + sum_noch
                total_chas = den_chas + noch_chas
                a.total_hours = total_chas
                kol_den_chas = den_chas
                kol_nosh_chas = noch_chas
                a.kol_noch = kol_nosh_chas
                a.kol_den = kol_den_chas
                a.den = sum_den
                a.noch = sum_noch
                a.total_sum = summa
            elif noch_fin <= nachalo < konec <= noch_start1:
                # Если  время переработок между 06 и 22
                den_chas = konec - nachalo
                sum_den = den_chas * 1.5 * cena_chasa
                summa = sum_den
                total_chas = den_chas
                kol_den_chas = den_chas
                a.kol_den = kol_den_chas
                a.total_hours = total_chas
                a.den = sum_den
                a.total_sum = summa
            elif noch_start <= nachalo < konec <= noch_fin:
                # Если  время начала переработок между 00 и 06
                noch_chas = noch_fin - nachalo
                sum_noch = noch_chas * 2 * cena_chasa
                summa = sum_noch
                total_chas = noch_chas
                a.total_hours = total_chas
                kol_nosh_chas = noch_chas
                a.kol_noch = kol_nosh_chas
                a.noch = sum_noch
                a.total_sum = summa
            elif noch_start1 <= nachalo < konec <= noch_fin1:
                # Если  время начала переработок между 22 и 23:59
                noch_chas = noch_fin1 - nachalo
                sum_noch = noch_chas * 2 * cena_chasa
                summa = sum_noch
                total_chas = noch_chas
                a.total_hours = total_chas
                kol_nosh_chas = noch_chas
                a.kol_noch = kol_nosh_chas
                a.noch = sum_noch
                a.total_sum = summa
            a.per_to_brigada_id = int(b.name[1])
            a.save()
        elif date_s < date_f:
            if noch_start <= nachalo <= noch_fin and noch_start <= konec <= noch_fin:
                # Если  время начала переработок между 00 и 06 и конец между 00 и 06 следующего дня
                noch_chas = (noch_fin - nachalo) + (noch_fin1 - noch_start1) + konec
                den_chas = noch_start1 - noch_fin
                sum_noch = noch_chas * 2 * cena_chasa
                sum_den = den_chas * 1.5 * cena_chasa
                summa = sum_den + sum_noch
                total_chas = den_chas + noch_chas
                kol_den_chas = den_chas
                kol_nosh_chas = noch_chas
                a.kol_noch = kol_nosh_chas
                a.kol_den = kol_den_chas
                a.total_hours = total_chas
                a.den = sum_den
                a.noch = sum_noch
                a.total_sum = summa
            elif noch_start <= nachalo <= noch_fin and noch_fin <= konec <= noch_start1:
                # Если  время начала переработок между 00 и 06 и конец между 06 и 22 следующего дня
                noch_chas = (noch_fin - nachalo) + (noch_fin1 - noch_start1) + noch_fin
                den_chas = (noch_start1 - noch_fin) + (konec - noch_fin)
                sum_noch = noch_chas * 2 * cena_chasa
                sum_den = den_chas * 1.5 * cena_chasa
                summa = sum_den + sum_noch
                total_chas = den_chas + noch_chas
                kol_den_chas = den_chas
                kol_nosh_chas = noch_chas
                a.kol_noch = kol_nosh_chas
                a.kol_den = kol_den_chas
                a.total_hours = total_chas
                a.den = sum_den
                a.noch = sum_noch
                a.total_sum = summa
            elif noch_start <= nachalo <= noch_fin and noch_start1 <= konec <= noch_fin1:
                # Если  время начала переработок между 00 и 06 и конец между 22 и 24 следующего дня
                noch_chas = (noch_fin - nachalo) + (noch_fin1 - noch_start1) + noch_fin + (konec - noch_start1)
                den_chas = (noch_start1 - noch_fin) + (noch_start1 - noch_fin)
                sum_noch = noch_chas * 2 * cena_chasa
                sum_den = den_chas * 1.5 * cena_chasa
                summa = sum_den + sum_noch
                total_chas = den_chas + noch_chas
                kol_den_chas = den_chas
                kol_nosh_chas = noch_chas
                a.kol_noch = kol_nosh_chas
                a.kol_den = kol_den_chas
                a.total_hours = total_chas
                a.den = sum_den
                a.noch = sum_noch
                a.total_sum = summa
            elif noch_fin <= nachalo <= noch_start1 and noch_start <= konec <= noch_fin:
                # Если  время начала переработок между 06 и 22 и конец между 00 и 06 следующего дня
                noch_chas = (noch_fin1 - noch_start1) + konec
                den_chas = noch_start1 - nachalo
                sum_noch = noch_chas * 2 * cena_chasa
                sum_den = den_chas * 1.5 * cena_chasa
                summa = sum_den + sum_noch
                total_chas = den_chas + noch_chas
                kol_den_chas = den_chas
                kol_nosh_chas = noch_chas
                a.kol_noch = kol_nosh_chas
                a.kol_den = kol_den_chas
                a.total_hours = total_chas
                a.den = sum_den
                a.noch = sum_noch
                a.total_sum = summa
            elif noch_fin <= nachalo <= noch_start1 and noch_fin <= konec <= noch_start1:
                # Если  время начала переработок между 06 и 22 и конец между 06 и 22 следующего дня
                noch_chas = (noch_fin1 - noch_start1) + (noch_fin - noch_start)
                den_chas = (noch_start1 - nachalo) + (konec - noch_fin)
                sum_noch = noch_chas * 2 * cena_chasa
                sum_den = den_chas * 1.5 * cena_chasa
                summa = sum_den + sum_noch
                total_chas = den_chas + noch_chas
                kol_den_chas = den_chas
                kol_nosh_chas = noch_chas
                a.kol_noch = kol_nosh_chas
                a.kol_den = kol_den_chas
                a.total_hours = total_chas
                a.den = sum_den
                a.noch = sum_noch
                a.total_sum = summa
            elif noch_fin <= nachalo <= noch_start1 and noch_start <= konec <= noch_fin1:
                # Если  время начала переработок между 06 и 22 и конец между 22 и 24 следующего дня
                noch_chas = (noch_fin1 - noch_start1) + (noch_fin - noch_start) + (konec - noch_start1)
                den_chas = (noch_start1 - nachalo) + (noch_start1 - noch_fin)
                sum_noch = noch_chas * 2 * cena_chasa
                sum_den = den_chas * 1.5 * cena_chasa
                summa = sum_den + sum_noch
                total_chas = den_chas + noch_chas
                kol_den_chas = den_chas
                kol_nosh_chas = noch_chas
                a.kol_noch = kol_nosh_chas
                a.kol_den = kol_den_chas
                a.total_hours = total_chas
                a.den = sum_den
                a.noch = sum_noch
                a.total_sum = summa
            elif noch_start1 <= nachalo <= noch_fin1 and noch_start <= konec <= noch_fin:
                # Если  время начала переработок между 22 и 24 и конец между 00 и 06 следующего дня
                noch_chas = (noch_fin1 - nachalo) + konec
                sum_noch = noch_chas * 2 * cena_chasa
                summa = sum_noch
                total_chas = noch_chas
                kol_nosh_chas = noch_chas
                a.kol_noch = kol_nosh_chas
                a.total_hours = total_chas
                a.noch = sum_noch
                a.total_sum = summa
            elif noch_start1 <= nachalo <= noch_fin1 and noch_fin <= konec <= noch_start1:
                # Если  время начала переработок между 22 и 24 и конец между 06 и 22 следующего дня
                noch_chas = (noch_fin1 - nachalo) + noch_fin
                den_chas = konec - noch_fin
                sum_noch = noch_chas * 2 * cena_chasa
                sum_den = den_chas * 1.5 * cena_chasa
                summa = sum_noch + sum_den
                total_chas = den_chas + noch_chas
                kol_den_chas = den_chas
                kol_nosh_chas = noch_chas
                a.kol_noch = kol_nosh_chas
                a.kol_den = kol_den_chas
                a.total_hours = total_chas
                a.den = sum_den
                a.noch = sum_noch
                a.total_sum = summa
            elif noch_start1 <= nachalo <= noch_fin1 and noch_start1 <= konec <= noch_fin1:
                # Если  время начала переработок между 22 и 24 и конец между 22 и 24 следующего дня
                noch_chas = (noch_fin1 - nachalo) + (noch_fin - noch_start) + (konec - noch_start1)
                den_chas = noch_start1 - noch_fin
                sum_noch = noch_chas * 2 * cena_chasa
                sum_den = den_chas * 1.5 * cena_chasa
                summa = sum_den + sum_noch
                total_chas = den_chas + noch_chas
                kol_den_chas = den_chas
                kol_nosh_chas = noch_chas
                a.kol_noch = kol_nosh_chas
                a.kol_den = kol_den_chas
                a.total_hours = total_chas
                a.den = sum_den
                a.noch = sum_noch
                a.total_sum = summa
            a.per_to_brigada_id = int(b.name[1])
            a.save()

        elif date_s > date_f:
            args['time_error'] = 'Дата начала переработок больше даты окончания'

    return render_to_response('add_pererabotka.html', args)
