1. Создать новую миграцию с автоматическим обнаружением изменений:

```shell
alembic revision --autogenerate -m "Название миграции"
```
2. Применить миграции:

```shell
alembic upgrade head
```

3. Откатить миграции (на одну миграцию назад):

```shell
alembic downgrade -1
```

4. Посмотреть историю миграций:

```shell
alembic history
```

5. Создать базу данных (если используется SQLAlchemy):

```shell
alembic create
```

6. Создать новую пустую миграцию без автоматического обнаружения изменений:

```shell
alembic revision -m "Название миграции"
```

