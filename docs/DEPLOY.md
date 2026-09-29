# Деплой Site-FastAPI на VPS

## Требования к серверу

- Ubuntu 22.04 LTS (или новее)
- 2 vCPU, 2GB RAM минимум
- 20GB SSD disk
- Docker 24+ и Docker Compose v2.20+

## Шаг 1: Подготовка сервера

```bash
# Обновить систему
sudo apt update && sudo apt upgrade -y

# Установить Docker
curl -fsSL https://get.docker.com | sudo sh

# Добавить пользователя в группу docker (заменить 'deploy' на вашего пользователя)
sudo usermod -aG docker deploy

# Перелогиниться или: newgrp docker

# Проверить установку
docker --version
docker compose version
```

## Шаг 2: Настройка проекта

```bash
# Клонируем репозиторий
cd /opt
git clone <repo-url> Site-FastAPI
cd Site-FastAPI

# Копируем продакшен конфиг
cp .env.production.example .env

# Редактируем .env — меняем секретные значения:
# - SECRET_KEY (генерируем: openssl rand -hex 32)
# - DATABASE_URL → postgresql+asyncpg://user:pass@db:5432/site
# - GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET
# - GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
# - TELEGRAM_BOT_TOKEN
# - FRONTEND_URL → https://yourdomain.com
```

## Шаг 3: Настройка Docker Compose

Файл `docker/docker-compose.yml` содержит три сервиса:

| Сервис | Порт | Назначение |
|---|---|---|
| `backend` | :8000 (внутри контейнера) | FastAPI API |
| `frontend` | :3000 (внутри контейнера) | Next.js App |
| `nginx` | :80, :443 | Reverse proxy + SSL |

### PostgreSQL (опционально для продакшена)

Для продакшена рекомендую заменить SQLite на PostgreSQL:

```yaml
# Добавить в docker-compose.yml:
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: site
      POSTGRES_USER: siteuser
      POSTGRES_PASSWORD: <strong-password>
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U siteuser"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  pgdata:
```

И обновить `DATABASE_URL` в `.env`:
```
DATABASE_URL=postgresql+asyncpg://siteuser:<strong-password>@db:5432/site
```

## Шаг 4: Настройка Nginx и SSL (Let's Encrypt)

### Установка Certbot

```bash
sudo apt install certbot python3-certbot-nginx -y
```

### Конфигурация Nginx

Файл `docker/nginx.conf` уже настроен для проксирования:
- `/api/` → backend:8000
- `/` → frontend:3000

### Получение SSL сертификата

```bash
# Запустить без SSL сначала
sudo docker compose -f docker/docker-compose.yml up -d --build

# Получить сертификат (nginx должен работать на порту 80)
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Certbot автоматически обновит nginx.conf и настроит редирект на HTTPS

# Проверить автообновление
sudo certbot renew --dry-run
```

### Ручная настройка SSL в nginx.conf

Если certbot не сработал автоматически:

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

    # ... остальные location блоки из nginx.conf
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
curl -s http://localhost:80/health  # backend health
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

## Резервное копирование

### База данных

```bash
#!/bin/bash
# backup.sh — добавить в cron (ежедневно в 3:00)
BACKUP_DIR="/opt/Site-FastAPI/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# SQLite бэкап
cp /opt/Site-FastAPI/site.db "$BACKUP_DIR/site_$DATE.db"

# Или PostgreSQL бэкап
# docker compose exec db pg_dump -U siteuser site > "$BACKUP_DIR/site_$DATE.sql"

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
sudo docker compose -f docker/docker-compose.yml logs -f nginx
```

### Проверка здоровья

```bash
# Backend health endpoint
curl -s http://localhost:80/health | jq

# Frontend доступность
curl -s -o /dev/null -w "%{http_code}" http://localhost/

# SSL сертификат (дней до истечения)
echo | openssl s_client -servername yourdomain.com -connect yourdomain.com:443 2>/dev/null | \
  openssl x509 -noout -dates
```

## Устранение неполадок

### Backend не запускается

```bash
# Проверить логи
sudo docker compose logs backend

# Проверить переменные окружения
sudo docker compose exec backend env | grep DATABASE_URL

# Пересобрать
sudo docker compose -f docker/docker-compose.yml up -d --build --no-cache backend
```

### Frontend не собирается

```bash
# Логи сборки
sudo docker compose logs frontend

# Проверить next.config.js — должен быть output: 'standalone'
```

### Nginx 502 Bad Gateway

```bash
# Проверить что backend и frontend запущены
sudo docker ps

# Проверить nginx конфиг
sudo docker compose exec nginx nginx -t

# Перезагрузить nginx
sudo docker compose exec nginx nginx -s reload
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
