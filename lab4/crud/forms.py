from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from .models import Books, Author
from .service.book import validate_book_form, validate_book_update_form


class BookForm(forms.ModelForm):
    author = forms.ModelChoiceField(queryset=Author.objects.all(), empty_label="Оберіть автора")

    # Додали валідатори для поля year
    year = forms.IntegerField(validators=[
        MinValueValidator(1000),  # Мінімальний рік
        MaxValueValidator(2024)  # Максимальний рік
    ])

    class Meta:
        model = Books
        fields = ['title', 'author', 'year']

    def clean(self):
        cleaned_data = super().clean()
        errors = validate_book_form(cleaned_data)
        if errors:
            for field, message in errors.items():
                self.add_error(field, message)

        return cleaned_data

    def clean_year(self):
        year = self.cleaned_data.get('year')
        title = self.cleaned_data.get('title')

        if year is not None:  # Перевірка на наявність поля 'year'
            errors = validate_book_update_form({'year': year,"title":title})
            print("errors:",errors)
            if errors:
                raise forms.ValidationError(errors['year'])

        return year


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'surname', 'birth_year', 'bio']
        labels = {
            'name': 'Ім\'я',
            'surname': 'Прізвище',
            'birth_year': 'Рік народження',
            'bio': 'Біографія'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть ім\'я'}),
            'surname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть прізвище'}),
            'birth_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Введіть рік народження'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введіть біографію', 'rows': 3}),
        }