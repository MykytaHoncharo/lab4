from django.contrib import admin

from .models import Author, Books

#admin.site.register(Author)
#admin.site.register(Books)

class BooksInstanceInline(admin.TabularInline):
    extra = 1
    model = Books

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["__str__", 'birth_year']
    list_filter = ['birth_year']
    inlines = [BooksInstanceInline]


@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    list_display = ["title", 'year', "display_author"]
    list_filter = ['year']
