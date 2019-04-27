from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import random
import os
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from pustakalaywebsite.utils import unique_slug_generator  
from django.urls import reverse  


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "books/{final_filename}".format(
            final_filename=final_filename
            )

class BookQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def search(self, query, searchFilter):
        if searchFilter == 'Title':
            lookups = Q(title__icontains=query)
        elif searchFilter == 'Author':
            lookups = Q(author__icontains=query)
        elif searchFilter == 'Isbn10/13':
            lookups = Q(isbn10__iexact=query) | Q(isbn13__iexact=query)
        elif searchFilter == 'Publisher':
            lookups = Q(publisher__icontains=query)
        elif searchFilter == 'None':
            lookups = (Q(title__icontains=query) | 
                  Q(author__icontains=query) |
                  Q(isbn10__iexact=query) | 
                  Q(isbn13__iexact=query) |
                  Q(publisher__icontains=query) | 
                  Q(tag__title__icontains=query))
        return self.filter(lookups).distinct()
    
class BookManager(models.Manager):
    def get_queryset(self):
        return BookQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id) # Product.objects == self.get_queryset()
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query, searchFilter):
        return self.get_queryset().active().search(query, searchFilter)


class Book(models.Model):

    def __str__(self):
        return self.title
    
    @property
    def name(self):
        return self.title
    
    def get_absolute_url(self):
#         return "/books/{slug}/".format(slug=self.slug)
          return reverse("books:booksdetail", kwargs={"slug": self.slug})

    def is_inventory_available(self):
        return not self.inventory <= 0  

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
    slug = models.SlugField(blank=True, unique=True)
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
    active = models.BooleanField(default=True)
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

    objects = BookManager()
    
def book_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
    instance.rank = (0.2 * instance.numberOfCopiesSold) + (0.4 * instance.pustakalayRating) + (0.1 * instance.avgcustomerRating) + (0.3 * instance.newArrival)


pre_save.connect(book_pre_save_receiver, sender=Book)

class Tag(models.Model):
    title       = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, unique=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    active      = models.BooleanField(default=True)
    books    = models.ManyToManyField(Book, blank=True)

    def __str__(self):
        return self.title

def tag_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(tag_pre_save_receiver, sender=Tag)
