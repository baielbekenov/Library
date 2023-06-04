from django.urls import path
from .views import *


urlpatterns = [
    path('', base, name='base'),
    path('index/<int:pk>/', index, name='index'),
    path('book_detail/<int:pk>/', book_detail, name='book_detail'),
    path('register/', register, name='register'),
    path('login/', loginpage, name='login'),
    path('logout/', logoutpage, name='logout'),
    path('createIsudoc/', createIsudoc, name='createIsudoc'),
    path('addblock/', addbook, name='addbook'),
    path('addcategory/', addcategory, name='addcategory'),
    path('issue_docs/', get_issue_docs, name='issue_docs'),
    path('isudoclist/', IssuedDocumentListView.as_view(), name='isudoclist'),
    path('export_excel/int:rows/', export_excel, name='export_excel'),
    path('search_results/', search, name='search_results'),
    path('send_message/', send_message, name='send_message'),
    path('search/', Search.as_view(), name='search'),

]