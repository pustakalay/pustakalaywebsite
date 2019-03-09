from django.shortcuts import render
from django.views.generic import ListView
from booksapp.models import Book

# Create your views here.

class SearchBookListView(ListView):
    template_name = "search/view.html"
    
    def get_queryset(self, *args, **kwargs):
        request = self.request
        if request.GET.get('q') is not None:
            return Book.objects.filter(title__icontains=request.GET.get('q')).order_by('-rank') 
        return None
