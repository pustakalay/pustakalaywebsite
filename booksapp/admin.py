from django.contrib import admin
from .models import Book, Tag

# Not working
class BookAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'slug']
    class Meta:
        model = Book

admin.site.register(Book)
admin.site.register(Tag)
