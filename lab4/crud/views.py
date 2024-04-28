from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from .forms import BookForm, AuthorForm
from .models import Books, Author



@login_required
def index(request):
    return render(request, 'crud/base.html', {'block_name': 'crud/template_menu.html'})
@login_required
def read(request):
    books = Books.objects.all()  # Отримуємо всі книги з бази даних
    search_query = request.GET.get('q', '')  # Отримуємо пошуковий запит з GET-параметра 'q'

    if search_query:
        # Якщо є пошуковий запит, фільтруємо книги за назвою
        books = books.filter(title__icontains=search_query)

    context = {
        'books': books,
        'block_name': 'crud/template_read.html',
    }
    return render(request, 'crud/base.html', context)

@login_required
def create(request):
    if request.user.is_admin() or request.user.is_manager():
        if request.method == 'POST':
            form = BookForm(request.POST)
            if form.is_valid():
                book = form.save()
                return redirect('read_books')
            else:
                print("Помилка")
                #return redirect('book_list')
        else:
            form = BookForm()

            # Фільтрація авторів за введеним ім'ям
        author_name = request.GET.get('author_name', '')
        authors = Author.objects.filter(name__icontains=author_name)

        context = {
            'form': form,
            'block_name': 'crud/template_create.html',
            'authors': authors
        }

        return render(request, 'crud/base.html', context)
    else:
        return redirect('home')

@login_required
def delete(request, book_id):
    if request.user.is_admin() or request.user.is_manager():
        book = get_object_or_404(Books, pk=book_id)
        if request.method == 'POST':
            book.delete()
            return redirect('read_books')

        context = {
            'book': book,
            'block_name': 'crud/template_delete.html',
            'book_id': book_id,  # Додайте це поле у контекст
        }
        return render(request, 'crud/base.html', context)
    else:
        return redirect('home')


@login_required
def update(request, book_id):
    if request.user.is_admin() or request.user.is_manager():
        book = get_object_or_404(Books, pk=book_id)

        if request.method == 'POST':
            form = BookForm(request.POST, instance=book)
            if form.is_valid():
                form.save()
                return redirect('read_books')
            else:
                print('Form is not valid')
        else:
            form = BookForm(instance=book)

        authors = Author.objects.all()  # Отримуємо всіх авторів

        context = {
            'book': book,
            'form': form,
            'authors': authors,  # Передаємо авторів у контекст
            'block_name': 'crud/template_update.html',
        }
        return render(request, 'crud/base.html', context)
    else:
        return redirect('home')


#---------------------------CBV-----------------------------

def class_view_decorator(decorator):
    def _decorator(cls):
        cls.dispatch = method_decorator(decorator)(cls.dispatch)
        return cls
    return _decorator
@class_view_decorator(login_required)
class AuthorListView(View):
    def get(self, request):
        authors = Author.objects.all()
        search_query = request.GET.get('q', '')
        if search_query:
            authors = authors.filter(name__icontains=search_query)
        return render(request, 'crud/base.html', {'authors': authors,"block_name":'crud/template_author_read.html'})

@class_view_decorator(login_required)
class AuthorCreateView(View):
    def get(self, request):
        if request.user.is_admin() or request.user.is_manager():
            form = AuthorForm()
            author_name = request.GET.get('author_name', '')
            authors = Author.objects.filter(name__icontains=author_name)
            return render(request, 'crud/base.html', {'form': form, 'authors': authors, "block_name":'crud/template_author_create.html'})
        else:
            return redirect('home')
    def post(self, request):
        if request.user.is_admin() or request.user.is_manager():
            form = AuthorForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('read_authors')
            else:
                return render(request, 'crud/base.html', {'form': form, "block_name":'crud/template_author_create.html'})
        else:
            return redirect('home')
@class_view_decorator(login_required)
class AuthorDeleteView(View):
    def get(self, request, author_id):
        if request.user.is_admin() or request.user.is_manager():
            author = get_object_or_404(Author, pk=author_id)
            return render(request, 'crud/base.html', {'author': author, "block_name":'crud/template_author_delete.html'})
        else:
            return redirect('home')
    def post(self, request, author_id):
        if request.user.is_admin() or request.user.is_manager():
            author = get_object_or_404(Author, pk=author_id)
            author.delete()
            return redirect('read_authors')
        else:
            return redirect('home')
@class_view_decorator(login_required)
class AuthorUpdateView(View):
    def get(self, request, author_id):
        if request.user.is_admin() or request.user.is_manager():
            author = get_object_or_404(Author, pk=author_id)
            form = AuthorForm(instance=author)
            return render(request, 'crud/base.html', {'form': form, 'author': author, "block_name":'crud/template_author_update.html'})
        else:
            return redirect('home')

    def post(self, request, author_id):
        if request.user.is_admin() or request.user.is_manager():
            author = get_object_or_404(Author, pk=author_id)
            form = AuthorForm(request.POST, instance=author)
            if form.is_valid():
                form.save()
                return redirect('read_authors')
            else:
                print(form.errors)
                return render(request, 'crud/base.html', {'form': form, 'author': author, "block_name":'crud/template_author_update.html'})

        else:
            return redirect('home')

