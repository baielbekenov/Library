from barcode import generate
from barcode.base import Barcode
from django.core.mail import message
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from PIL import Image
from django.views.decorators.http import require_POST
from django.views.generic import FormView, ListView, CreateView

from library.forms import IssuedDocumentForm, BookFilterForm, MessageSendForm
from library.models import User, Book, Barcode, IssuedDocument, Message, Room


# Create your views here.
def index(request):
    queryset = User.objects.all()
    context = {'queryset': queryset}
    return render(request, 'index.html', context)


class IssuedDocumentCreateView(CreateView):
    model = IssuedDocument
    template_name = 'createIsudoc.html'
    form_class = IssuedDocumentForm
    success_url = reverse_lazy('isudoclist')


class IssuedDocumentListView(ListView):
    model = IssuedDocument
    template_name = 'isudoclist.html'
    context_object_name = 'issuedoc'

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_param = self.request.GET.get('filter', '')
        if filter_param:
            queryset = queryset.filter(name__icontains=filter_param)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', '')
        return context


def search(request):
    books = Book.objects.all()
    form = BookFilterForm(request.GET)
    book_titles = []
    if form.is_valid():
        name = form.cleaned_data.get('name')
        author = form.cleaned_data.get('author')
        izdat = form.cleaned_data.get('izdat')
        category = form.cleaned_data.get('category')
        invented_number = form.cleaned_data.get('invented_number')
        if name:
            books = books.filter(name__icontains=name)
        if author:
            books = books.filter(author__icontains=author)
        if izdat:
            books = books.filter(izdat__icontains=izdat)
        if category:
            books = books.filter(category__name__icontains=category)
        if invented_number:
            books = books.filter(invented_number__icontains=invented_number)
        book_titles = set([book.name for book in books])
    context = {'books': books, 'form': form, 'book_titles': book_titles}
    return render(request, 'search_results.html', context)


def rooms(request):
    return render(request, "rooms.html")

def room(request, room_name):
    return render(request, "room.html", {"room_name": room_name})




