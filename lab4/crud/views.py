from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from .forms import BookForm, AuthorForm
from .models import Books, Author


def index(request):
    return render(request, 'crud/base.html', {'block_name': 'crud/template_menu.html'})

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

def create(request):
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

def delete(request, book_id):
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


def update(request, book_id):
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


#---------------------------CBV-----------------------------

class AuthorListView(View):
    def get(self, request):
        authors = Author.objects.all()
        search_query = request.GET.get('q', '')
        if search_query:
            authors = authors.filter(name__icontains=search_query)
        return render(request, 'crud/base.html', {'authors': authors,"block_name":'crud/template_author_read.html'})

class AuthorCreateView(View):
    def get(self, request):
        form = AuthorForm()
        author_name = request.GET.get('author_name', '')
        authors = Author.objects.filter(name__icontains=author_name)
        return render(request, 'crud/base.html', {'form': form, 'authors': authors, "block_name":'crud/template_author_create.html'})

    def post(self, request):
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('read_authors')
        else:
            return render(request, 'crud/base.html', {'form': form, "block_name":'crud/template_author_create.html'})

class AuthorDeleteView(View):
    def get(self, request, author_id):
        author = get_object_or_404(Author, pk=author_id)
        return render(request, 'crud/base.html', {'author': author, "block_name":'crud/template_author_delete.html'})

    def post(self, request, author_id):
        author = get_object_or_404(Author, pk=author_id)
        author.delete()
        return redirect('read_authors')

class AuthorUpdateView(View):
    def get(self, request, author_id):
        author = get_object_or_404(Author, pk=author_id)
        form = AuthorForm(instance=author)
        return render(request, 'crud/base.html', {'form': form, 'author': author, "block_name":'crud/template_author_update.html'})

    def post(self, request, author_id):
        author = get_object_or_404(Author, pk=author_id)
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            return redirect('read_authors')
        else:
            print(form.errors)
            return render(request, 'crud/base.html', {'form': form, 'author': author, "block_name":'crud/template_author_update.html'})