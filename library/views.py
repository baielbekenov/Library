from django.contrib import messages
from django.contrib.auth import get_user_model, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import Http404, HttpResponse

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from django.views.generic import ListView, CreateView

from library.forms import BookFilterForm, UserRegisterForm, IssuedDocumentForm
from library.models import Message, Thread, IssuedDocument, Book, Barcode, Category

User = get_user_model()

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('/')
        print(form.errors)
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = UserRegisterForm()
    return render(request=request, template_name="register.html", context={"register_form": form})


def loginpage(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form": form})


class ThreadView(View):
    template_name = 'chat.html'

    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)

    def get_object(self):
        other_username  = self.kwargs.get("username")
        self.other_user = get_user_model().objects.get(username=other_username)
        obj = Thread.objects.get_or_create_personal_thread(self.request.user, self.other_user)
        if obj == None:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = {}
        context['me'] = self.request.user
        context['thread'] = self.get_object()
        context['user'] = self.other_user
        context['messages'] = self.get_object().message_set.all()
        return context

    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context=context)

    def post(self, request, **kwargs):
        self.object = self.get_object()
        thread = self.get_object()
        data = request.POST
        user = request.user
        text = data.get("message")
        Message.objects.create(sender=user, thread=thread, text=text)
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context=context)


# Create your views here.
def index(request):
    queryset = User.objects.all()
    context = {'queryset': queryset}
    return render(request, 'index.html', context)


def base(request):
    category = Category.objects.all()
    context = {'category': category}
    return render(request, 'base.html', context)


class IssuedDocumentCreateView(CreateView):
    model = IssuedDocument
    template_name = 'createIsudoc.html'
    form_class = IssuedDocumentForm
    success_url = reverse_lazy('isudoclist')

def createIsudoc(request):
    if request.method == 'POST':
        form = IssuedDocumentForm(request.POST)
        if form.is_valid():
            form.save()

            return HttpResponse('Добавлено')
    else:
        form = IssuedDocumentForm()

    context = {'form': form}
    return render(request, 'createIsudoc.html', context)


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




