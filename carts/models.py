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
            if request.user.is_authenticated() and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            new_obj = True
            cart_obj = Cart.objects.new(user=request.user)
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj
    
    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated():
                user_obj = user
        return self.model.objects.create(user=user_obj)

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
        
def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        books = instance.books.all()
        total = 0
        for x in books:
            total += x.price
        if instance.subtotal != total:
            instance.subtotal = total
            instance.save()

m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.books.through)

def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    if instance.subtotal > 0:
        instance.total = float(instance.subtotal) * float(1.10) # 10% tax)
    else:
        instance.total = 0.00
pre_save.connect(pre_save_cart_receiver, sender=Cart)

def post_save_cart_receiver(sender, instance, *args, **kwargs):
    if instance.books.count() != 0:
        for book in instance.books.all():
            if not book.is_inventory_available():
                instance.books.remove(book)
                instance.books_removed.add(book)
                
post_save.connect(post_save_cart_receiver, sender=Cart)