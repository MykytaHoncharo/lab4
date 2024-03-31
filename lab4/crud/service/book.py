def validate_book_form(data):
    errors = {}

    title = data.get('title')
    if not title:

        errors['title'] = 'Поле "Назва" є обов\'язковим'

    author_id = data.get('author')
    if not author_id:
        errors['author'] = 'Поле "Автор" є обов\'язковим'

    year = data.get('year')
    if year is None or year < 1000 or year > 2024:
        errors['year'] = 'Рік публікації повинен бути у діапазоні від 1000 до 2024'

    return errors


def validate_book_update_form(data):
    errors = {}

    title = data.get('title')
    if not title:
        errors['title'] = 'Поле "Назва" є обов\'язковим'

    year = data.get('year')
    if year is None or year < 1000 or year > 2024:
        errors['year'] = 'Рік публікації повинен бути у діапазоні від 1000 до 2024'

    return errors