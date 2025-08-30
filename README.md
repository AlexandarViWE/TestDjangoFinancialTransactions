# Веб-сервис для управления движением денежных средств 
## Описание 

Для использования приложения необходимо иметь доступ к аккаунту **суперпользователя**.

## Запуск проекта 

> :warning: **Это исключительно для разработки, не для "продакшена"**!

### Установка зависимостей.
```shell
pip install -r requirements.txt
```

### Настройка базы данных
Миграция базы данных.
```shell
python manage.py migrate
```

Создание суперпользователя. Для доступа к интерфейсу управления финансовыми транзакциями необходимо создать супер пользователя. 
```shell
python manage.py createsuperuser
```

### Запуск сервера
Запуск сервера.
```shell
python manage.py runserver
```

## Ссылки

Автозаполнение в django admin:
https://forum.djangoproject.com/t/dependent-drop-down/16558
https://stackoverflow.com/questions/57143113/how-to-use-the-admin-autocomplete-field-in-a-custom-form
 
