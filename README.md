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

## Требования

- Docker Engine 20.10+
- Docker Compose Plugin (встроен в Docker 20.10+)

### Установка Docker (если не установлен)

**Ubuntu / Debian:**
```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
# Перелогиньтесь или выполните: newgrp docker
```

**Проверка:**
```bash
docker --version
docker compose version
```

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
docker compose up --build -d
```

Дождитесь завершения сборки (первый раз ~2-5 минут).

### 4. Создание администратора
```bash
docker exec -it babyblog_web python manage.py createsuperuser
```

### 5. Открыть в браузере
| Страница | URL |
|----------|-----|
| Сайт | http://localhost |
| Админка Django | http://localhost/admin/ |
| Модерация | http://localhost/moderation/ |
| Почта (тест) | http://localhost:8025 |

## Полезные команды

```bash
# Статус контейнеров
docker compose ps

# Логи веб-сервера
docker compose logs -f web

# Логи всех сервисов
docker compose logs -f

# Остановка
docker compose down

# Остановка с удалением всех данных (БД, медиа)
docker compose down -v

# Перезапуск после изменений кода
docker compose restart web

# Бэкап базы данных
docker exec -it babyblog_web python manage.py dumpdata --indent 2 > backup.json

# Применить миграции вручную
docker exec -it babyblog_web python manage.py migrate
```

## Устранение проблем

**`docker-compose: command not found`**
Используйте `docker compose` (без дефиса). В новых версиях Docker Compose встроен как плагин.

**`docker: command not found`**
Установите Docker: `curl -fsSL https://get.docker.com | sh`

**`permission denied`**
Добавьте пользователя в группу docker: `sudo usermod -aG docker $USER` и перелогиньтесь.

**Порт 80 занят**
Измените порт nginx в `docker-compose.yml`: замените `"80:80"` на `"8080:80"`, затем откройте http://localhost:8080
