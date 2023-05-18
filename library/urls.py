from django.urls import path
from .views import *


urlpatterns = [
    path('', base, name='base'),
    path('index/', index, name='index'),
    path('register/', register, name='register'),
    path('login/', loginpage, name='login'),
    path('createIsudoc/', createIsudoc, name='createIsudoc'),
    path('isudoclist/', IssuedDocumentListView.as_view(), name='isudoclist'),
    path('search_results/', search, name='search_results'),
    path('<str:username>/', ThreadView.as_view(), name='chat'),

]