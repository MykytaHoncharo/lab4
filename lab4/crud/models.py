from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

def Validate_year(year):
    current_year = timezone.now().year
    if year > current_year:
        raise ValidationError("Рік не може бути більшим ніж поточний!")
class Author(models.Model):
    name = models.CharField("Ім'я",max_length=50)
    surname = models.CharField("Прізвище",max_length=50)
    birth_year = models.IntegerField("Рік народження",validators=[Validate_year])
    bio = models.CharField("Біографія",max_length=400)

    def __str__(self):
        return str(self.name) + " " + str(self.surname)


    class Meta:
        verbose_name="Автор"
        verbose_name_plural="Автори"

class Books(models.Model):
    title = models.CharField("Назва",max_length=50)
    year = models.IntegerField("Рік видання",validators=[Validate_year])
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def display_author(self):
        return self.author.__str__()
    display_author.short_description = "Автор"

    class Meta:
        verbose_name="Книга"
        verbose_name_plural="Книги"


