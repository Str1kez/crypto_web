# Бэк для лабы по защите инфы

## Получить соль для .env файла

```commandline
echo "..." | md5sum | clipc
```

## Запуск
### Ну тут ваще изи, нужен Poetry

- Устанавливаем пакеты
- Поднимаем бд
- Миграция
- Запуск

```commandline
poetry install
make db
make upgrade head
make run
```

