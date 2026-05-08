1. Установка и настройка .venv
`python -m venv .venv`
`.venv\Scripts\activate`

2. Установка Django и Pillow
`pip install Django`
`pip install Pillow`

3. Миграции и запуск сервера
`cd djangoblog`
`python manage.py migrate`
`python manage.py runserver`

4. Создание суперпользователя
`python manage.py createsuperuser`