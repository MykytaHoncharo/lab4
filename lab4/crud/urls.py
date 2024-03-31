from django.urls import path
from . import views
from .views import AuthorCreateView, AuthorDeleteView, AuthorUpdateView, AuthorListView

urlpatterns = [
    path('', views.index, name = 'home'),
    path('create', views.create, name = 'create'),
    path('read/', views.read, name='read_books'),
    path('update/<int:book_id>/', views.update, name='update_book'),
    path('delete/<int:book_id>/', views.delete, name='delete_book'),

    path('author/create', AuthorCreateView.as_view(), name='create_author'),
    path('author/read/', AuthorListView.as_view(), name='read_authors'),
    path('author/update/<int:author_id>/', AuthorUpdateView.as_view(), name='update_author'),
    path('author/delete/<int:author_id>/', AuthorDeleteView.as_view(), name='delete_author'),

]