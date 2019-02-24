from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import random
import os

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1,3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "books/{final_filename}".format( 
            final_filename=final_filename
            )


class Book(models.Model):

    def __str__(self):
        return self.title

    LANGUAGE_CHOICES = (
        ('HINDI', 'Hindi'),
        ('ENGLISH', 'English'),
        ('MARATHI', 'Marathi')
    )
    FORMAT_CHOICES = (
        ('PAPERBACK', 'Paperback'),
        ('HARDCOVER', 'Hardcover'),
        ('EBOOK', 'Ebook')
    )
    title = models.CharField(max_length=200)
    displayTitle = models.CharField(max_length=200, blank=True)
    author = models.CharField(max_length=200)
    language = models.CharField(max_length=200, choices=LANGUAGE_CHOICES, default='English')
    format = models.CharField(max_length=200, choices=FORMAT_CHOICES, default='Paperback')
    publisher = models.CharField(max_length=200)
    publishingDate = models.DateField(blank=True)
    isbn10 = models.CharField(max_length=200, unique=True, blank=True)
    isbn13 = models.CharField(max_length=200, unique=True, blank=True)
    dimension = models.CharField(max_length=200)
    weight = models.FloatField()
    numberOfPages = models.BigIntegerField()
    category = models.CharField(max_length=200, blank=True)
    subCategory = models.CharField(max_length=200, blank=True)
    edition = models.CharField(max_length=200, blank=True)
    numberOfCopiesSold = models.BigIntegerField(default=0)
    pustakalayRating = models.FloatField(default=0, validators=[MaxValueValidator(5), MinValueValidator(1)])
    avgcustomerRating = models.BigIntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(1)])
    newArrival = models.FloatField(default=0, validators=[MaxValueValidator(5), MinValueValidator(1)])  # #auto decrement
    context = models.CharField(max_length=200, blank=True)
    rank = models.FloatField(default=0)
    translatedBy = models.CharField(max_length=200, blank=True)
    sku = models.CharField(default='pu', max_length=200, unique=True, blank=True)
    price = models.BigIntegerField(default=200)
    maxretailprice = models.BigIntegerField(default=200)
    minimumprice = models.BigIntegerField(default=200)
    discount = models.BigIntegerField(default=200)
    inventory = models.BigIntegerField(default=200)
    description = models.TextField(max_length=20000)
    author = models.CharField(max_length=200)
    aboutAuthor = models.TextField(max_length=20000, blank=True)
    image_front = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    image_back = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
