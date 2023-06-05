import datetime
import xlwt
from django.contrib import messages
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import Http404, HttpResponse

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View

from django.views.generic import ListView, CreateView

from library.forms import BookFilterForm, UserRegisterForm, IssuedDocumentForm, MessageForm, BookForm, CategoryForm
from library.models import Message, IssuedDocument, Book, Barcode, Category

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

def logoutpage(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def index(request, pk):
    books = Book.objects.all().filter(category=pk)
    filtered_books = Book.objects.all().filter(category=pk, is_digital=True)
    context = {'books': books, 'filtered_books': filtered_books}
    return render(request, 'index.html', context)


@login_required(login_url='login')
def book_detail(request, pk):
    try:
        book = Book.objects.get(id=pk)
    except ObjectDoesNotExist:
        book = None

    context = {
        'book': book,
    }
    return render(request, 'book_detail.html', context)


@login_required(login_url='login')
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
            createisu = form.save(commit=False)
            book = get_object_or_404(Book, id=createisu.name_id)
            use = get_object_or_404(User, id=createisu.name_of_reader_id)
            createisu.author_document = book.author
            createisu.book_name = book.name
            createisu.izdat_year = book.created_year
            createisu.name_of_lib = book.category
            createisu.name_of_reader2 = use.first_name + ' ' + use.last_name
            createisu.group = use.group
            createisu.semester = use.semester
            createisu.number_read_bilet = use.number_read_bilet
            createisu.id_student = use.id_student

            form.save()

            return redirect('/')
    else:
        form = IssuedDocumentForm()

    context = {'form': form}
    return render(request, 'createIsudoc.html', context)

@login_required(login_url='login')
def addbook(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()

            return HttpResponse('Добавлено')
    else:
        form = BookForm()
    context = {'form': form}
    return render(request, 'addbook.html', context)


def export_excel(rows):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Expenses' + \
        str(datetime.datetime.now()) + '.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Expenses')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Название книги', 'Автор', 'Год издания', 'Дата выдачи книг',
               'Дата возврата книг', 'Фактическая дата возврата', 'ФИО получателя',
               'Группа', 'Семестер',
               'Номер читательского билета', 'ID студента', 'Названия библиотеки']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = IssuedDocument.objects.all().values_list('book_name', 'author_document', 'izdat_year', 'date_issued',
                                                    'date_give', 'fact_give', 'name_of_reader2', 'group', 'semester',
                                                    'number_read_bilet', 'id_student', 'name_of_lib')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)

    return response


def users(request):
    user = User.objects.all()
    context = {'user': user}
    return render(request, 'users.html', context)


@login_required(login_url='login')
def addcategory(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()

            return HttpResponse('Добавлено')
    else:
        form = CategoryForm()
    context = {'form': form}
    return render(request, 'addcategory.html', context)


def get_issue_docs(request):
    issue_docs = IssuedDocument.objects.filter(name_of_reader=request.user)
    context = {'issue_docs': issue_docs}
    return render(request, 'issue_docs.html', context)


def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user  # присваиваем текущего пользователя автором
            message.save()
            return redirect('base')
    else:
        form = MessageForm()
    return render(request, 'chat.html', {'form': form})


def message(request):
    messages = Message.objects.all()
    context = {'messages': messages}
    return render(request, 'chat.html', context)


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

@login_required(login_url='login')
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


class Search(ListView):
    paginated_by = 3
    template_name = 'book_search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Book.objects.filter(Q(name__icontains=query))
        return object_list

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['q'] = self.request.GET.get('q')
        return context

