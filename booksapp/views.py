from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Book
from django.http import Http404
from django.http import HttpResponseRedirect
from django.urls import reverse


class BookListView(ListView):
    queryset = Book.objects.all().order_by('-rank')
    template_name = "booksapp/list.html"
    
class BookDetailView(DetailView):
    queryset = Book.objects.all()
    template_name = "booksapp/details.html"

def buyBook(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    book.numberOfCopiesSold  += 1
    book.save()
    return HttpResponseRedirect(reverse('bookapp:index'))