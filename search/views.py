from django.views.generic import ListView
from booksapp.models import Book
from carts.models import Cart

# Create your views here.

class SearchBookListView(ListView):
    template_name = "search/view.html"
    
    def get_context_data(self, *args, **kwargs):
        context = super(SearchBookListView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context
    
    def get_queryset(self, *args, **kwargs):
        request = self.request
        if request.GET.get('q') is not None:
            return Book.objects.search(request.GET.get('q'),request.GET.get('f')).order_by('-rank') 
        return None
