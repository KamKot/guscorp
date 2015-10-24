# coding=utf-8
from django.db import models

# Create your models here.

BRIGADA_CHOICES = (
    ('1', '1 бригада'),
    ('2', '2 бригада'),
    ('3', '2 бригада'),
)

class brigada(models.Model):
    class Meta():
        db_table = 'brigada'

    name = models.TextField(verbose_name='Имя сотрудника')

class pererabotka(models.Model):
    class Meta():
        db_table = 'pererabotka'

    per_to_brigada = models.ForeignKey(brigada)
    p_id = models.CharField(max_length=1, verbose_name='ID бригады', choices=BRIGADA_CHOICES)
    p_date_start = models.DateField(verbose_name='Дата начала выезда')
    p_time_start = models.TimeField(verbose_name='Время начала выезда')
    p_date_finish = models.DateField(verbose_name='Дата окончания выезда')
    p_time_finish = models.TimeField(verbose_name='Время окончания выезда')
    p_address = models.TextField(verbose_name='Адрес выезда')
    p_description = models.TextField(verbose_name='Описание заявки')
    hours_cost = models.FloatField(default=173.5)
    den = models.FloatField(verbose_name='Количество дневных часов', default=0)
    noch = models.FloatField(verbose_name='Количество ночных часов', default=0)
    total_hours = models.FloatField(default=1)
    total_sum = models.FloatField(default=0)


class start(models.Model):
    class Meta():
        db_table = 'start'

    start_text = models.TextField(verbose_name='Приветственный текст')
    start_description = models.TextField(verbose_name='Текст-ссылка')