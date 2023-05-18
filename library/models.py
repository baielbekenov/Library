from datetime import timezone, datetime
from io import BytesIO
import barcode
from barcode.writer import ImageWriter
from django.core.files import File
from django.db import models
from django.contrib.auth.models import AbstractUser

from library.managers import ThreadManager


class User(AbstractUser):
    is_employee = models.BooleanField(verbose_name=('Сотрудник'), default=False)
    is_simple_user = models.BooleanField(verbose_name=('Пользователь'), default=False)

    def __str__(self):
        return self.username


class Barcode(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    barcode = models.ImageField(upload_to='images/', verbose_name='Баркод изображения', blank=True)
    country_id = models.CharField(max_length=1, null=True)
    manufactured_id = models.CharField(max_length=6, null=True)
    number_id = models.CharField(max_length=5, null=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        EAN = barcode.get_barcode_class('ean13')
        ean = EAN(f'{self.country_id}{self.manufactured_id}{self.number_id}', writer=ImageWriter())
        buffer = BytesIO()
        ean.write(buffer)
        self.barcode.save('barcode.png', File(buffer), save=False)
        return super().save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    image = models.ImageField(upload_to='photos', verbose_name='Изображения', blank=True, null=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    author = models.CharField(max_length=100, verbose_name='Автор', default='Неизвестно')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория', default='')
    barcode = models.ForeignKey(Barcode, on_delete=models.CASCADE, verbose_name='Баркод')
    is_digital = models.BooleanField(default=False, verbose_name='Цифровой')
    file = models.FileField(verbose_name='Файл', blank=True, null=True)
    tom = models.IntegerField(verbose_name='Том', blank=True, null=True)
    part = models.CharField(max_length=50, verbose_name='Часть', blank=True, null=True)
    izdat = models.CharField(max_length=100, verbose_name='Издательство', blank=True, null=True)
    place = models.CharField(max_length=100, verbose_name='Место', blank=True, null=True)
    created_year = models.DateField()
    amount_of_pages = models.IntegerField(verbose_name='Количество страниц', blank=True, null=True)
    invented_number = models.IntegerField(verbose_name='Инвентарный номер', blank=True, null=True)

    def __str__(self):
        return self.name


class IssuedDocument(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название книги')
    author_document = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор книги')
    izdat_year = models.DateField(verbose_name='Год издания книги')
    date_issued = models.DateField(verbose_name='Дата выдачи документа')
    name_of_reader = models.CharField(max_length=150, verbose_name='ФИО получателя')
    number_read_bilet = models.IntegerField(verbose_name='Номер читательского билета')
    name_of_lib = models.CharField(max_length=100, verbose_name='Названия библиотеки')

    def __str__(self):
        return self.name


    def __str__(self):
        return self.name



class TrackingModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Thread(TrackingModel):
    THREAD_TYPE = (
        ('personal', 'Personal'),
        ('group', 'Group')
    )

    name = models.CharField(max_length=50, null=True, blank=True)
    thread_type = models.CharField(max_length=15, choices=THREAD_TYPE, default='group')
    users = models.ManyToManyField(User)

    objects = ThreadManager()

    def __str__(self) -> str:
        if self.thread_type == 'personal' and self.users.count() == 2:
            return f'{self.users.first()} and {self.users.last()}'
        return f'{self.name}'


class Message(TrackingModel):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=False, null=False)

    def __str__(self) -> str:
        return f'From <Thread - {self.thread}>'