from django.contrib import admin

from .models import Author, Books

admin.site.register(Author)
admin.site.register(Books)
