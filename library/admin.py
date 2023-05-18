from django.contrib import admin
from library.models import User, Message, Thread, Barcode, Book, IssuedDocument, Category

# Register your models here.
admin.site.register(User)
admin.site.register(Barcode)
admin.site.register(Book)
admin.site.register(IssuedDocument)
admin.site.register(Category)
admin.site.register(Message)
admin.site.register(Thread)
