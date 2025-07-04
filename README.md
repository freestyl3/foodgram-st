# Foodgram

Проект Фудграм разработан в качестве учебного проекта финального спринта для курса от Яндекса **Ассоциированные программы: бэкенд-разработчик**.

## Автор проекта

**Алексей Тягущев**

**Github: [github.com/freestyl3](github.com/freestyl3)**

## Для запуска проекта необходимо:

### Шаг 1: Копирование репозитория

```
git clone github.com/freestyl3/foodgram-st
cd foodgram-st
```

### Шаг 2: Создание .env файла

```
touch .env
```

Откройте файл в любом текстовом редакторе и отредактируйте в соответствии с примером:

```
POSTGRES_USER=example_user
POSTGRES_PASSWORD=yourmegasecretpassword
POSTGRES_DB=example_db
DB_HOST=db
DB_PORT=5432
```

### Шаг 3: Разворачивание проекта в контейнерах

Чтобы развернуть проект необходимо перейти в PowerShell или WSL

Чтобы развернуть проект необходимо выполнить команды:

```
cd infra
docker compose up --build
```

Обязательно дождитесь, чтобы применились все миграции и фикстуры, а также nginx был готов принимать запросы.

Все миграции и фикстуры применяются автоматически после того, как база данных будет готова принимать запросы, это может занять некоторое время.

### Шаг 4: Создание суперпользователя

Находясь в этой же директории и с работающей сетью контейнеров, выполните команду (можно открыть другой терминал) и следуйте инструкциям:

```
docker compose exec backend python manage.py createsuperuser
```

### Шаг 5: Доступ к сервису

* Фудграм: [http://localhost/](http://localhost/)
* Админ-зона: [http://localhost/admin](http://localhost/admin)
* Документация API: [http://localhost/api/docs](http://localhost/api/docs)

### Шаг 6: Остановка и удаление сервиса

Чтобы остановить сервис необходимо в директории `/foodgram-st/infra` выполнить команду:

```
docker compose stop
```

Для удаления сервиса необходимо выполнить команды:

```
docker compose rm
docker volume rm infra_postgres_data infra_media infra_static
```