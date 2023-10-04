## Запуск проекта
Склонируйте себе репозиторий:
`git clone git@github.com:kubanez-create/Lenta_TS_backend.git`

Перейдите в созданную папку:
`cd Lenta_TS_backend`

Для запуска проекта требуется создать 1 (один) .env файл, лежащий в корне проекта, рядом с
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

Выполните команду `docker compose up -d --build`
После запуска контейнера последовательно выполните команды:

```bash
sudo docker-compose exec web python manage.py migrate
sudo docker-compose exec web python manage.py createsuperuser
sudo docker-compose exec web python manage.py collectstatic --no-input
sudo docker compose exec backend python manage.py loadcsv product /app/data/pr_df.csv
sudo docker compose exec backend python manage.py loadcsv shop /app/data/st_df.csv
sudo docker compose exec backend python manage.py loadcsv sales /app/data/sales_df_train_trunkated.csv
```