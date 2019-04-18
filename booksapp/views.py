from django.views.generic import ListView, DetailView
from .models import Book
from carts.models import Cart
from analytics.mixins import ObjectViewedMixin
from django.contrib.auth.mixins import LoginRequiredMixin

class UserProductHistoryView(LoginRequiredMixin, ListView):
    template_name = "booksapp/user-history.html"
    def get_context_data(self, *args, **kwargs):
        context = super(UserProductHistoryView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        views = request.user.objectviewed_set.by_model(Book, model_queryset=False)
        return views

class BookListView(ListView):
    queryset = Book.objects.all().order_by('-rank')
    template_name = "booksapp/list.html"
    
    def get_context_data(self, *args, **kwargs):
        context = super(BookListView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context
    
class BookDetailView(ObjectViewedMixin, DetailView):
    queryset = Book.objects.all()
    def get_context_data(self, *args, **kwargs):
        context = super(BookDetailView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context
    template_name = "booksapp/details.html"