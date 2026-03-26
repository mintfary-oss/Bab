# BabyBlog — Сообщество для беременных

Django + PostgreSQL + Docker Compose. Полнофункциональная самохостинговая платформа.

## Возможности

- Регистрация, профили, аватары
- Дневник (посты, комментарии, лайки, черновики)
- Трекер беременности (42 недели, развитие плода, чек-листы)
- Каталог роддомов (поиск, фильтры, отзывы)
- Друзья, чаты, группы, уведомления
- Админ-панель, модерация, настройки оформления
- Полнотекстовый поиск
- Резервное копирование

## Быстрый старт

### 1. Клонирование
```bash
git clone https://github.com/mintfary-oss/Bab.git
cd Bab
```

### 2. Настройка окружения
```bash
cp .env.example .env
```
Файл `.env` уже содержит все настройки для локального запуска. Ничего менять не нужно.

> Для продакшна рекомендуется заменить `DJANGO_SECRET_KEY` и `POSTGRES_PASSWORD` на свои значения.

### 3. Запуск
```bash
docker-compose up --build -d
```

### 4. Создание администратора
```bash
docker exec -it babyblog_web python manage.py createsuperuser
```

### 5. Открыть в браузере
- Сайт: http://localhost
- Админка: http://localhost/admin/
- Почта (тест): http://localhost:8025

## Полезные команды

```bash
# Логи
docker-compose logs -f web

# Остановка
docker-compose down

# Остановка с удалением данных
docker-compose down -v

# Перезапуск
docker-compose restart web

# Бэкап
docker exec -it babyblog_web python manage.py dumpdata --indent 2 > backup.json
```
