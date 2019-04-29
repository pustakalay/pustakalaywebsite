from django.conf import settings
from django.db import models
from booksapp.models import Book
from django.db.models.signals import pre_save, m2m_changed, post_save

User = settings.AUTH_USER_MODEL

class CartManager(models.Manager):
    
    def new_or_get(self,request):
        cart_id = request.session.get("cart_id", None)
        qs = self.filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
        else:
            if request.user.is_authenticated():
                cart_obj, new_obj = Cart.objects.get_or_create(user=request.user)
            else:                
                new_obj = True
                cart_obj = Cart.objects.create(user = None)
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj

class Cart(models.Model):
    user        = models.ForeignKey(User, null=True, blank=True)
    books       = models.ManyToManyField(Book, related_name="cart", through='BookQuantity', blank=True)
    books_removed = models.ManyToManyField(Book, related_name="removed_from_cart", through='BookRemovedQuantity', blank=True)
    subtotal    = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    total       = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    updated     = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    
    objects = CartManager()

    def __str__(self):
        return str(self.id)
    
    def get_books_count(self):
        quantity = 0
        for book_quantity in BookQuantity.objects.filter(cart=self):
            quantity = book_quantity.quantity + quantity
        return quantity
    
class BookQuantity(models.Model):
    cart = models.ForeignKey(Cart, related_name='book_quantity', on_delete=models.SET_NULL, null=True)
    book = models.ForeignKey(Book, related_name='book_quantity', on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return str(self.book.name)
    
class BookRemovedQuantity(models.Model):
    cart = models.ForeignKey(Cart, related_name='book_removed_quantity', on_delete=models.SET_NULL, null=True)
    book_removed = models.ForeignKey(Book, related_name='book_removed_quantity', on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField()
        
def post_save_book_quantity_receiver(sender, instance, *args, **kwargs):
    books = instance.cart.books.all()
    total = 0
    for x in books:
        book_quantity = BookQuantity.objects.get(cart=instance.cart,book=x)
        if book_quantity.quantity is not None:
            total += (x.price*book_quantity.quantity)
    if instance.cart.subtotal != total:
        instance.cart.subtotal = total
        instance.cart.save()

post_save.connect(post_save_book_quantity_receiver, sender=BookQuantity)

def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    if instance.subtotal > 0:
        instance.total = float(instance.subtotal) + 50 #Shipping Charges    
    else:
        instance.total = 0.00
pre_save.connect(pre_save_cart_receiver, sender=Cart)

def post_save_cart_receiver(sender, instance, *args, **kwargs):
    if instance.books.count() != 0:
        for book in instance.books.all():
            book_quantity = BookQuantity.objects.get(cart=instance,book=book)
            if book_quantity.quantity is not None:
                diff = book.inventory - book_quantity.quantity
                if (diff) < 0:                                                   
                    book_removed_quantity, created = BookRemovedQuantity.objects.get_or_create(cart=instance, book_removed=book, quantity = -diff)
                        
post_save.connect(post_save_cart_receiver, sender=Cart)