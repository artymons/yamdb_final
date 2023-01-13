![example workflow](https://github.com/artymons/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
### Описание проекта:

YAMDB - это каталог произведений совмещённый с обширной базой публикаций о них и возможностью оставлять свои отзывы обо всём на свете.
Для возможности самостоятельного расширения каталога реализована возможность скрытого внедерения тайтлов пользователями, а для админов даны широкие права и обязанности распределённые по ролям. Присоединяйтесь или оставьте свои комментарии на века.

### Как запустить проект:

Пример env:

```
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=yamd # имя базы данных
POSTGRES_USER=yamd # логин для подключения к базе данных
POSTGRES_PASSWORD=123456 # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
```

Сборка с запуском контенера:

```
зайтив в infra и выполнить - docker-compose up -d --build
```

Выполнить миграции:

```
docker-compose exec web python manage.py migrate
```

Создать суперпользователя

```
docker-compose exec web python manage.py createsuperuser
```
Теперь проект доступен по адресу http://localhost/

### Примеры запросов к api:

Создание пользователя
Запрос:
/api/v1/auth/signup/
Ответ:
{
  "email": "string",
  "username": "string"
}

Получение информации о произведении
Запрос:
/api/v1/titles/{titles_id}/
Ответ:
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}

Получение списка всех отзывов
Запрос:
/api/v1/titles/{title_id}/reviews/
Ответ:
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "text": "string",
        "author": "string",
        "score": 1,
        "pub_date": "2019-08-24T14:15:22Z"
      }
    ]
  }
]

Более подробное описание api можно найти в документации:
http://127.0.0.1:8000/redoc/
