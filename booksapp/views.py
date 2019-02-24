from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Book


class BookListView(ListView):
    queryset = Book.objects.all().order_by('-rank')
    template_name = "booksapp/list.html"
    
class BookDetailView(DetailView):
    queryset = Book.objects.all()
    template_name = "booksapp/details.html"