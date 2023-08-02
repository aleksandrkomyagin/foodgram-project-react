<div align=center>
  
# [Foodgram](https://foodgram-top.sytes.net/)

![Python](https://img.shields.io/badge/Python-3.9.10-blue)
![Django](https://img.shields.io/badge/Django-3.2.3-blue)
![Django_REST_framework](https://img.shields.io/badge/Django_REST_framework-3.14.0-blue)
![Nginx](https://img.shields.io/badge/Nginx-1.18.0-blue)
![Gunicorn](https://img.shields.io/badge/Gunicorn-20.1.0-blue)
![Djoser](https://img.shields.io/badge/Djoser-2.2.0-blue)
![Postgres](https://img.shields.io/badge/Postgres-13.10-blue)
![React](https://img.shields.io/badge/React-blue)
</div>


## Описание проекта

Foodgram - онлайн-сервис и API для него, на котором пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Особенности реализации
* Проект развернут с использованием Docker и docker-compose.
* Для запуска использовались два официальных образа(nginx и postgres) и 2 разработанных образа(foodgram_backend и foodgram_frontend). Образы храняться на DockerHub
* Реализован workflow c автодеплоем на удаленный сервер и отправкой сообщения в Telegram

## Ресурсы API

* Ресурс **recipes**: все рецепты
* Ресурс **recipes/create**: создание рецепта
* Ресурс **recipes/favorite**: список избранных рецептов
* Ресурс **recipes/subscriptions**: список подписок на авторов рецептов
* Ресурс **recipes/shopping_cart**: список покупок


<details>
  <summary>
    <h2>Запуск проекта на локальном сервере</h2>
  </summary>

> Для MacOs и Linux вместо python использовать python3

1. Клонировать репозиторий.
   ```
       $ git@github.com:aleksandrkomyagin/foodgram-project-react.git
   ```
2. Создать и активировать виртуальное окружение.
   ```
       $ cd backend
       $ python -m venv venv
   ```
   Для Windows:
   ```
       $ source venv/Scripts/activate
   ```
   Для MacOs/Linux:
   ```
       $ source venv/bin/activate
   ```
2. Запустить docker-compose из дирректории infra.Перед запуском в корне проекта создать файл .env, по шаблону(в корне проекта файл .env.example).
    ```
        $ docker-compose up --build
    ```
3. Создать миграции, собрать статику и загрузить список ингредиентов в базу.
    ```
        $ docker-compose exec backend python manage.py migrate
        $ docker-compose exec backend python manage.py collectstatic
        $ docker-compose exec backend python manage.py load_data
    ```
4. Создать суперпользователя и через админ панель создать хотя бы 1 тег.
    ```
        $ docker-compose exec backend python manage.py createsuperuser
    ```
- После выполнения вышеперечисленных инструкций бэкенд проекта будет доступен по адресу http://127.0.0.1:8080/
- Документация проекта доступна по адресу http://127.0.0.1:8080/api/docs/
- Почта и пароль от админки: admin@mail.ru/admin

</details>

---

<div align=center>

## Контакты

[![Telegram Badge](https://img.shields.io/badge/-aleksandrkomyagin8-blue?style=social&logo=telegram&link=https://t.me/aleksandrkomyagin8)](https://t.me/aleksandrkomyagin8) [![Gmail Badge](https://img.shields.io/badge/-aleksandrkomyagin8@gmail.com-c14438?style=flat&logo=Gmail&logoColor=white&link=mailto:aleksandrkomyagin8@gmail.com)](mailto:aleksandrkomyagin8@gmail.com)

</div>
