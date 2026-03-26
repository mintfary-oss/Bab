# BabyBlog — Сообщество для беременных

Django + PostgreSQL + Docker Compose.

## Быстрый старт

```bash
git clone https://github.com/mintfary-oss/Bab.git
cd Bab
cp .env.example .env
docker compose up --build -d
```

Дождитесь запуска (~2-3 минуты). Затем создайте администратора:

```bash
docker exec -it babyblog_web python manage.py createsuperuser
```

Откройте в браузере:
- Сайт: http://ваш-ip
- Админка: http://ваш-ip/admin/
- Почта (тест): http://ваш-ip:8025

## Обновление после git pull

```bash
docker compose down
git pull origin main
cp .env.example .env
docker compose up --build -d
```

## Полезные команды

```bash
# Статус
docker compose ps

# Логи
docker compose logs -f web

# Остановка
docker compose down

# Полная пересборка с нуля
docker compose down -v
docker compose up --build -d
```

## Возможности

- Регистрация, профили, аватары
- Дневник (посты, комментарии, лайки, черновики)
- Трекер беременности (42 недели, развитие плода, чек-листы)
- Каталог роддомов (поиск, фильтры, отзывы)
- Друзья, чаты, группы, уведомления
- Админ-панель, модерация, настройки оформления
- Полнотекстовый поиск
- Резервное копирование
