from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('createIsudoc/', IssuedDocumentCreateView.as_view(), name='createIsudoc'),
    path('isudoclist/', IssuedDocumentListView.as_view(), name='isudoclist'),
    path('search_results/', search, name='search_results'),
    ]