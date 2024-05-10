# MAGWED


### Magazine wedding


## Описание проекта

Портал, помогающий молодоженам найти организаторов свадьбы в желаемом городе. Это своего рода социальная сеть, с просмотром организаторов, фотоальбомов, фотографий, лайками, отзывами, комментариями, чатом и прочим.


## Установка

Для запуска проекта испльзуется Docker.

##### 1. Клонировать репозиторий

    git clone https://github.com/andreibaliyevich/MAGWED.git

##### 2. Перейти в папку репозитория

    cd MAGWED

##### 3. Создать файл .env с переменными окружения в папке backend

Например:

    SECRET_KEY=secret_key
    SQL_NAME=sql_name
    SQL_USER=sql_user
    SQL_PASSWORD=sql_password
    EMAIL_HOST_USER=email_host_user
    EMAIL_HOST_PASSWORD=email_host_password
    EMAIL_HOST_RECEIVER=email_host_receiver

##### 4. Создать файл .env с переменными окружения в папке frontend:

    NODE_OPTIONS=--no-warnings

##### 5. Создать файл .env с переменными окружения в папке postgres

Например:

    POSTGRES_DB=sql_name
    POSTGRES_USER=sql_user
    POSTGRES_PASSWORD=sql_password

##### 6. Создать образ

    docker compose build

##### 7. Запустить bash в сервисе backend

    docker compose run backend bash

##### 8. Применить миграции

    python manage.py migrate

##### 9. Скомпилировать файлы переводов

    django-admin compilemessages

##### 10. Создать суперпользователя

    python manage.py createsuperuser

##### 11. Выйти из bash

    exit

##### 12. Запустить контейнер

    docker compose up


## Лицензия

[GNU General Public License version 3](https://opensource.org/licenses/GPL-3.0)

Copyright © 2022 Andrei Baliyevich
