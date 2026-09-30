# Деплой Site-FastAPI на VPS

## Требования к серверу

- Ubuntu 22.04 LTS (или новее)
- 2 vCPU, 2GB RAM минимум
- 20GB SSD disk
- Docker 24+ и Docker Compose v2.20+
- nginx на хосте (reverse proxy, ВНЕ docker-compose)

## Архитектура

```
Internet → host nginx :80/:443 → 127.0.0.1:8000 (backend, docker)
                               → 127.0.0.1:3000 (frontend, docker)
                               → db (postgres, только внутренняя сеть, без внешних портов)
```

Reverse proxy работает на хосте, а не в docker-compose. Пример конфига:
`docker/nginx.host.conf.example`.

## Шаг 1: Подготовка сервера

```bash
# Обновить систему
sudo apt update && sudo apt upgrade -y

# Установить Docker
curl -fsSL https://get.docker.com | sudo sh

# Добавить пользователя в группу docker (заменить 'deploy' на вашего пользователя)
sudo usermod -aG docker deploy

# Перелогиниться или: newgrp docker

# Установить nginx на хост
sudo apt install nginx -y

# Проверить установку
docker --version
docker compose version
nginx -v
```

## Шаг 2: Настройка проекта

```bash
# Клонируем репозиторий
cd /opt
git clone <repo-url> Site-FastAPI
cd Site-FastAPI

# Копируем продакшен конфиг
cp .env.production.example docker/.env.production

# Если меняете POSTGRES_USER/POSTGRES_PASSWORD/POSTGRES_DB — продублируйте их
# в docker/.env: compose-интерполяция ${POSTGRES_*} читает именно docker/.env
cp docker/.env.production docker/.env

# Редактируем docker/.env.production — меняем секретные значения:
# - POSTGRES_PASSWORD (сильный пароль БД)
# - SECRET_KEY (генерируем: openssl rand -hex 32)
# - GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET
# - GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
# - TELEGRAM_BOT_TOKEN
# - FRONTEND_URL → https://yourdomain.com
```

Схема БД создаётся автоматически: entrypoint контейнера backend выполняет
`alembic upgrade head` против PostgreSQL перед запуском uvicorn. Ручная
инициализация не требуется.

## Шаг 3: Docker Compose

Файл `docker/docker-compose.yml` содержит три сервиса:

| Сервис | Порт | Назначение |
|---|---|---|
| `backend` | 127.0.0.1:8000 | FastAPI API |
| `frontend` | 127.0.0.1:3000 | Next.js App |
| `db` | только внутренняя сеть | PostgreSQL 17 |

Порты backend/frontend публикуются только на 127.0.0.1 — их проксирует хостовой
nginx. База данных не публикуется наружу вообще.

## Шаг 4: Настройка host nginx и SSL (Let's Encrypt)

### Конфигурация nginx

```bash
sudo cp docker/nginx.host.conf.example /etc/nginx/sites-available/site-fastapi
sudo nano /etc/nginx/sites-available/site-fastapi   # указать server_name
sudo ln -s /etc/nginx/sites-available/site-fastapi /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl reload nginx
```

Пример проксирует:
- `/api/` → 127.0.0.1:8000 (backend)
- `= /health` → 127.0.0.1:8000/health
- `/` → 127.0.0.1:3000 (frontend)

### Получение SSL сертификата

```bash
sudo apt install certbot python3-certbot-nginx -y

# Стек должен быть запущен, nginx отвечает на порту 80
sudo docker compose -f docker/docker-compose.yml up -d --build
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Certbot автоматически обновит конфиг nginx и настроит редирект на HTTPS

# Проверить автообновление
sudo certbot renew --dry-run
```

### Ручная настройка SSL в nginx

Если certbot не сработал автоматически, добавьте в server-блок хостового nginx:

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # SSL настройки
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # ... те же location блоки, что в docker/nginx.host.conf.example
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$host$request_uri;
}
```

## Шаг 5: Запуск продакшена

```bash
# Собрать и запустить
sudo docker compose -f docker/docker-compose.yml up -d --build

# Проверить статус
sudo docker compose -f docker/docker-compose.yml ps

# Просмотр логов
sudo docker compose -f docker/docker-compose.yml logs -f

# Проверить health checks
curl -s http://127.0.0.1:8000/health   # backend напрямую
curl -s http://localhost/health        # через host nginx
```

## Шаг 6: Настройка автозапуска

```bash
# Создать systemd сервис для автозапуска Docker Compose
sudo tee /etc/systemd/system/site-fastapi.service > /dev/null <<EOF
[Unit]
Description=Site-FastAPI Docker Compose
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/Site-FastAPI
ExecStart=/usr/bin/docker compose -f docker/docker-compose.yml up -d
ExecStop=/usr/bin/docker compose -f docker/docker-compose.yml down

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable site-fastapi
sudo systemctl start site-fastapi
```

## Миграции базы данных

При старте контейнера backend автоматически выполняется `alembic upgrade head`.

Запустить вручную (например, после git pull без пересборки):

```bash
sudo docker compose -f docker/docker-compose.yml exec backend \
  alembic -c backend/alembic.ini upgrade head
```

## Резервное копирование

### База данных

```bash
#!/bin/bash
# backup.sh — добавить в cron (ежедневно в 3:00)
BACKUP_DIR="/opt/Site-FastAPI/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# PostgreSQL бэкап
docker compose -f /opt/Site-FastAPI/docker/docker-compose.yml exec -T db \
  pg_dump -U siteuser site > "$BACKUP_DIR/site_$DATE.sql"

# Удалить бэкапы старше 30 дней
find "$BACKUP_DIR" -name "site_*" -mtime +30 -delete

echo "Backup completed: $DATE"
```

```bash
# Добавить в crontab
crontab -e
# Добавить строку:
0 3 * * * /opt/Site-FastAPI/backup.sh >> /var/log/site-backup.log 2>&1
```

### Docker volumes бэкап

```bash
# Бэкап всех docker данных
sudo tar -czf /opt/backups/docker_$(date +%Y%m%d).tar.gz /var/lib/docker/volumes/
```

## Обновление

```bash
cd /opt/Site-FastAPI
git pull origin main
sudo docker compose -f docker/docker-compose.yml up -d --build
```

## Мониторинг

### Проверка логов в реальном времени

```bash
sudo docker compose -f docker/docker-compose.yml logs -f backend
sudo docker compose -f docker/docker-compose.yml logs -f frontend
sudo docker compose -f docker/docker-compose.yml logs -f db
sudo tail -f /var/log/nginx/error.log   # хостовой nginx
```

### Проверка здоровья

```bash
# Backend health endpoint
curl -s http://localhost:8000/health | jq

# Frontend доступность
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/

# Через host nginx
curl -s http://localhost/health | jq

# SSL сертификат (дней до истечения)
echo | openssl s_client -servername yourdomain.com -connect yourdomain.com:443 2>/dev/null | \
  openssl x509 -noout -dates
```

## Устранение неполадок

### Backend не запускается

```bash
# Проверить логи (миграции alembic выполняются на старте — ошибки БД видны здесь)
sudo docker compose logs backend

# Проверить переменные окружения
sudo docker compose exec backend env | grep DATABASE_URL

# Проверить доступность БД
sudo docker compose exec db pg_isready -U siteuser -d site

# Пересобрать
sudo docker compose -f docker/docker-compose.yml up -d --build --no-cache backend
```

### Frontend не собирается

```bash
# Логи сборки
sudo docker compose logs frontend

# Проверить next.config.js — должен быть output: 'standalone'
```

### Host nginx 502 Bad Gateway

```bash
# Проверить что backend и frontend запущены и здоровы
sudo docker compose -f docker/docker-compose.yml ps

# Проверить что порты слушаются
ss -tlnp | grep -E '8000|3000'

# Проверить конфиг хостового nginx
sudo nginx -t

# Перезагрузить nginx
sudo systemctl reload nginx
```

### SSL проблемы

```bash
# Проверить сертификат
sudo certbot certificates

# Обновить сертификат
sudo certbot renew --force-renewal

# Проверить права на файлы сертификатов
ls -la /etc/letsencrypt/live/yourdomain.com/
```
