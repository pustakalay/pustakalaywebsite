from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from django.db import models
from django.db.models.signals import post_save, pre_delete
from accounts.signals import user_logged_in
from .signals import object_viewed_signal
from pustakalaywebsite.utils import get_client_ip
from django.core.exceptions import ObjectDoesNotExist
from carts.models import Cart, BookQuantity

User = settings.AUTH_USER_MODEL

FORCE_SESSION_TO_ONE = getattr(settings, 'FORCE_SESSION_TO_ONE', False)
FORCE_INACTIVE_USER_ENDSESSION= getattr(settings, 'FORCE_INACTIVE_USER_ENDSESSION', False)

class ObjectViewedQuerySet(models.query.QuerySet):
    def by_model(self, model_class, model_queryset=False):
        c_type = ContentType.objects.get_for_model(model_class)
        qs = self.filter(content_type=c_type)
        if model_queryset:
            viewed_ids = [x.object_id for x in qs]
            return model_class.objects.filter(pk__in=viewed_ids)
        return qs

class ObjectViewedManager(models.Manager):
    def get_queryset(self):
        return ObjectViewedQuerySet(self.model, using=self._db)

    def by_model(self, model_class, model_queryset=False):
        return self.get_queryset().by_model(model_class, model_queryset=model_queryset)

class ObjectViewed(models.Model):
    user                = models.ForeignKey(User, blank=True, null=True) # User instance instance.id
    ip_address          = models.CharField(max_length=220, blank=True, null=True) #IP Field
    content_type        = models.ForeignKey(ContentType) # User, Product, Order, Cart, Address
    object_id           = models.PositiveIntegerField() # User id, Product id, Order id,
    content_object      = GenericForeignKey('content_type', 'object_id') # Product instance
    timestamp           = models.DateTimeField(auto_now_add=True)

    objects = ObjectViewedManager()

    def __str__(self):
        return "%s viewed on %s" %(self.content_object, self.timestamp)

    class Meta:
        ordering = ['-timestamp'] # most recent saved show up first
        verbose_name = 'Object viewed'
        verbose_name_plural = 'Objects viewed'

def object_viewed_receiver(sender, instance, request, *args, **kwargs):
    c_type = ContentType.objects.get_for_model(sender) # instance.__class__     
    user = None
    if request.user.is_authenticated():
        user = request.user    
    ObjectViewed.objects.create(
                user = user,
                content_type=c_type,
                object_id=instance.id,
                ip_address = get_client_ip(request)
        )

object_viewed_signal.connect(object_viewed_receiver)

class UserSession(models.Model):
    user                = models.ForeignKey(User, blank=True, null=True) # User instance instance.id
    ip_address          = models.CharField(max_length=220, blank=True, null=True) #IP Field
    session_key         = models.CharField(max_length=100, blank=True, null=True) #min 50
    timestamp           = models.DateTimeField(auto_now_add=True)
    active              = models.BooleanField(default=True)
    ended               = models.BooleanField(default=False)

    def end_session(self):
        to_delete = True
        try:
            Session.objects.get(pk=self.session_key).delete()
        except ObjectDoesNotExist:
            to_delete = True
        except:
            to_delete = False
        finally:
            if to_delete:
                self.delete()
        return to_delete

def post_save_session_receiver(sender, instance, created, *args, **kwargs):
    if created:
        qs = UserSession.objects.filter(user=instance.user, ended=False, active=False).exclude(id=instance.id)
        for i in qs:
            i.end_session()
    if not instance.active and not instance.ended:
        instance.end_session()

if FORCE_SESSION_TO_ONE:
    post_save.connect(post_save_session_receiver, sender=UserSession)

def post_save_user_changed_receiver(sender, instance, created, *args, **kwargs):
    if not created:
        if instance.is_active == False:
            qs = UserSession.objects.filter(user=instance.user, ended=False, active=False)
            for i in qs:
                i.end_session()


if FORCE_INACTIVE_USER_ENDSESSION:
    post_save.connect(post_save_user_changed_receiver, sender=User)

def user_logged_in_receiver(sender, instance, request, *args, **kwargs):
    user = instance
    ip_address = get_client_ip(request)
    session_key = request.session.session_key # Django 1.11
    UserSession.objects.create(
            user=user,
            ip_address=ip_address,
            session_key=session_key
        )
    mergeCarts(user,request)

def mergeCarts(user,request):
    cart_id = request.session.get("cart_id", None)
    cart_qs = Cart.objects.filter(user=user)
    if cart_id is not None and cart_qs.exists():
        anonymous_cart = Cart.objects.filter(id=cart_id).first()
        user_cart = cart_qs.first()
        for anonymous_book_quantity in anonymous_cart.book_quantity.all():
            user_book_quantity, created = BookQuantity.objects.get_or_create(cart=user_cart, book=anonymous_book_quantity.book)
            if created:
                user_book_quantity.quantity = anonymous_book_quantity.quantity            
            else:
                user_book_quantity.quantity = user_book_quantity.quantity + anonymous_book_quantity.quantity
            user_book_quantity.save()
        request.session['cart_item_count'] = user_cart.get_books_count()        
        Cart.objects.filter(id=cart_id).delete()
        request.session['cart_id'] = user_cart.id

user_logged_in.connect(user_logged_in_receiver)

def sessionend_handler(sender, instance, **kwargs):
    try : 
        UserSession.objects.get(session_key = instance.session_key).delete()
    except:
        print("UserSession with session_key " +instance.session_key+" does not exist. ")

pre_delete.connect(sessionend_handler, sender=Session)