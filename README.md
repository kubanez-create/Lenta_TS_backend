# Foodcast

Бэкенд приложение для прогнозирования спроса на продукцию собственного производства "Лента".

На текущий момент позволяет авторизованным пользователям:
 - фильтровать данные по магазину, группе товаров, категории товаров, подкатегории товаров, и задавать диапазон дат;
 - просматривать и выгружать в файл excel прогноз продаж на продукцию собственного производства;
 - просматривать фактические продажи, предсказанные продажи и точность прошлых прогнозов

Помимо этого в автоматическом режиме ежедневно раз в день генерируются свежие прогнозные значения продаж в разрезе
магазин/скю и сохраняются в базу данных.

## Стек технологий
- Python
- Django
- Django REST Framework
- PostgreSQL
- Docker

## Зависимости
- Перечислены в файле foodcast/requirements.txt

## Для запуска на собственном сервере

1. Установите на сервере `docker` и `docker compose`;
2. Склонируйте себе репозиторий:
`git clone git@github.com:kubanez-create/Lenta_TS_backend.git`
3. Перейдите в созданную папку:
`cd Lenta_TS_backend`
4. Создайте в корне проекта файл `.env`;
Внесите в данный файл переменные окружения:
```bash
SECRET_KEY=<Ваш_секретный_ключ>
DB_ENGINE=<база_данных>
DB_NAME=<произвольное_имя_базы_данных>
POSTGRES_USER=<имя_пользователя_базы_данных>
POSTGRES_PASSWORD=<пароль_к_базе_данных>
DB_HOST=<хост_базы_данных>
DB_PORT=<порт_базы_данных>
# Переменная ответственная за переключение используемой базы данных
# на локальной машине мы пользуемся sqlite3 (true), в докере - postgresql
# (false)
DEVELOPMENT = false
```
5. Из корневой директории выполните команду `docker compose up -d --build`;
После запуска контейнера последовательно выполните команды (возможно потребуется прописать sudo)
```bash
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py createsuperuser
docker compose exec backend python manage.py collectstatic --no-input
docker compose exec backend python manage.py loadcsv product /app/data/pr_df.csv
docker compose exec backend python manage.py loadcsv shop /app/data/st_df.csv
# данные фактических продаж и прогнозные значения ограничены двумя магазинами
# c id 53e19f3dbb211f20b20b45668303c1b6, 42a0e188f5033bc65bf8d78622277c4e для
# ускорения заполнения базы данных
docker compose exec backend python manage.py loadcsv sales /app/data/sales_2_st.csv
docker compose exec backend python manage.py loadcsv forecasts /app/data/predictions_2_st.csv
```
6. После этого Вам должны быть доступны страницы с документацией http://localhost:8000/swagger/ и админка http://localhost:8000/admin/.

Получить токен можно как в swagger через обращение к /api/v1/auth/token/login, так и в админке в разделе Токенs.
Чтобы авторизоваться в swagger вставьте в поле Authorize
**token some_numbers_and_letters_your_token_consists_of** (cлово "token", затем пробел и значение токена).

## Авторы

- [Костенко Станислав](https://github.com/kubanez-create)
- [Курмашев Темирлан](https://github.com/timxt23)
