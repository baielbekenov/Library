from django.contrib import admin
from library.models import User, Barcode, Book, IssuedDocument, Order, Category, Message, Chat

# Register your models here.
admin.site.register(User)
admin.site.register(Barcode)
admin.site.register(Book)
admin.site.register(IssuedDocument)
admin.site.register(Order)
admin.site.register(Category)
admin.site.register(Message)
admin.site.register(Chat)
