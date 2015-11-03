#coding=utf-8
from django import forms
from django.forms import ModelForm
from pererabotka.models import pererabotka
from django.forms.extras.widgets import SelectDateWidget
from django.forms.extras import widgets
import calendar
from pererabotka.models import brigada
import datetime


BIRTH_YEAR_CHOICES = ('1980', '1981', '1982')
year = datetime.date.today().year
CHOICES = (('1', 'First',), ('2', 'Second',))
'''for i in brigada.name:
    CHOICES2 = (i, brigada.name[i])'''
FAVORITE_COLORS_CHOICES = (('blue', 'Blue'),
                            ('green', 'Green'),
                            ('black', 'Black'))

'''
class PerForm(forms.ModelForm):
    class Meta():
        birth_year = forms.DateField(widget=SelectDateWidget, label='День рождения')
        favorite_colors = forms.MultipleChoiceField(required=False,
                                                    widget=forms.CheckboxSelectMultiple,
                                                    choices=FAVORITE_COLORS_CHOICES)
        model = pererabotka
        fields = ['p_id', 'p_date_start', 'p_date_finish', 'p_address', 'p_description', 'hours_cost',
                  'total_hours', 'total_sum']
        vv = forms.ModelForm'''


class PerForm(forms.Form):
        #name = forms.ChoiceField(label='Имя сотрудника', widget=forms.SelectMultiple, choices=CHOICES)
        name = forms.ModelChoiceField(queryset=brigada.objects.values_list('id', 'name'), widget=forms.Select)
        p_id = forms.CharField(max_length=1, label='ID бригады')
        '''date_start = forms.DateField(label='Дата начала выезда', initial=datetime.date.today,
                                     widget=SelectDateWidget(years=range(year, year-5, 5)))'''
        date_start = forms.DateField(label='Дата начала выезда')
        time_start = forms.TimeField(label='Время начала выезда')
        date_finish = forms.DateField(label='Дата окончания выезда')
        time_finish = forms.TimeField(label='Время окончания выезда')
        address = forms.CharField(label='Адрес выезда')
        description = forms.CharField(label='Описание выезда', widget=forms.Textarea)
        p_hours_cost = forms.FloatField(label='Стоимость часа')
