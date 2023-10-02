## Запуск проекта

Для запуска проекта нужен 1 (один) .env файл, лежащий в корне проекта, рядом с
.gitignore и README.md.
Примерное, а может быть и точное содержание файла может быть таким:

```
SECRET_KEY = 'django-insecure-i4(m5feku5be-yn%r9h$r+bdnl6v4n@b+cy9myqs1iqn#p$6mn'
DB_ENGINE = django.db.backends.postgresql
DB_NAME = postgres
POSTGRES_USER = postgres
POSTGRES_PASSWORD = postgres
DB_HOST = db
DB_PORT = 5432
```
