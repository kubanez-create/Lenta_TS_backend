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
DEVELOPMENT = 1
```

Выполните команду `docker compose up -d --build`
После запуска контейнера последовательно выполните команды (возможно будет
необходимо прописать sudo перед каждой командой - в WSL2+Windows11 мне пришлось
прописывать sudo, в VM VirtualBox Manager + Ubuntu server, наоборот, работали
только команды без sudo).

```bash
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py createsuperuser
docker compose exec backend python manage.py collectstatic --no-input
docker compose exec backend python manage.py loadcsv product /app/data/pr_df.csv
docker compose exec backend python manage.py loadcsv shop /app/data/st_df.csv
sudo docker compose exec backend python manage.py loadcsv sales /app/data/sales_df_train_truncated.csv
sudo docker compose exec backend python manage.py loadcsv forecasts /app/data//sales_submission_trancated.csv
```

После этого Вам должны быть доступны страницы с документацией http://localhost:8000/swagger/ и
админка http://localhost:8000/admin/. Добавлять тестовые предсказания придется сегодня/завтра вручную в админке в разделе Прогнозы
продаж. В поле Прогнозы продаж, при добавлении нового прогноза нужно вставить следующую структуру данных:

```json
{
  "2023-09-01": 1,
  "2023-09-02": 3,
  "2023-09-03": 7,
  "2023-09-04": 9,
  "2023-09-05": 0
}
```

Получить токен можно как в swagger через обращение к /api/v1/auth/token/login, так и в админке в разделе Токенs.
Чтобы авторизоваться в swagger вставьте в поле Authorize
**token some_numbers_and_letters_your_token_consists_of** (cлово "token", затем пробел и значение токена).
