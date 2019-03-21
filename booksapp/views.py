from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Book
from django.http import Http404
from django.http import HttpResponseRedirect
from django.urls import reverse
from carts.models import Cart

class BookListView(ListView):
    queryset = Book.objects.all().order_by('-rank')
    template_name = "booksapp/list.html"
    
    def get_context_data(self, *args, **kwargs):
        context = super(BookListView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context
    
class BookDetailView(DetailView):
    queryset = Book.objects.all()
    def get_context_data(self, *args, **kwargs):
        context = super(BookDetailView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context
    template_name = "booksapp/details.html"

def buyBook(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    book.numberOfCopiesSold  += 1
    book.save()
    return HttpResponseRedirect(reverse('bookapp:index'))