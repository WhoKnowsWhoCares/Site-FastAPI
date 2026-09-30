# Site-FastAPI

Персональный сайт-портфолио с FastAPI бэкендом и Next.js фронтендом. Отображает проекты (AboutMe, iHome, Trade4Me, SD Art) и предоставляет защищённую админ-панель для управления контентом.

## Быстрый старт

### Требования

- Python 3.13+
- Node.js 18+
- uv (https://docs.astral.sh/uv/) — менеджер пакетов для Python
- Docker + Docker Compose (для контейнерной сборки)

### Установка и запуск

```bash
# Клонировать репозиторий
git clone <repo-url>
cd Site-FastAPI

# --- Бэкенд (из корня репозитория) ---
cp backend/.env.example backend/.env               # Скопировать конфиг (по умолчанию dev)
uv sync                                            # Установить зависимости
uv run uvicorn backend.main:app --reload   # Запуск на :8000

# --- Фронтенд ---
cd ../frontend
npm install                                 # Установить зависимости
npm run dev                                 # Запуск на :3000

# Тесты бэкенда
uv run pytest -v --cov=backend --cov-report=term-missing

# Линтинг
uv run ruff check .
```

### Docker

```bash
# Полная сборка (backend + frontend + nginx)
docker compose -f docker/docker-compose.yml up -d --build

# Просмотр логов
docker compose -f docker/docker-compose.yml logs -f

# Остановка
docker compose -f docker/docker-compose.yml down
```

## Переменные окружения

| Переменная | Описание | По умолчанию |
|---|---|---|
| `DATABASE_URL` | URL базы данных | `sqlite:///./site.db` |
| `SECRET_KEY` | Ключ для подписи JWT | `change-me-to-random-string-32-chars-min` |
| `FRONTEND_URL` | URL фронтенда (для OAuth redirect) | `http://localhost:3000` |
| `GITHUB_CLIENT_ID` | GitHub OAuth Client ID | — |
| `GITHUB_CLIENT_SECRET` | GitHub OAuth Client Secret | — |
| `GOOGLE_CLIENT_ID` | Google OAuth Client ID | — |
| `GOOGLE_CLIENT_SECRET` | Google OAuth Client Secret | — |
| `TELEGRAM_BOT_TOKEN` | Telegram Bot Token (для Login Widget) | — |

Пример: `.env.production.example` в корне репозитория.

## Структура проекта

```
Site-FastAPI/
├── backend/              # FastAPI, SQLAlchemy async, JWT/OAuth
│   ├── api/v1/          # Эндпоинты (auth, content, admin)
│   ├── services/        # Бизнес-логика
│   ├── models/          # SQLAlchemy модели
│   ├── schemas/         # Pydantic схемы
│   └── tests/           # pytest тесты (103 теста, 86% coverage)
├── frontend/            # Next.js 14+ App Router, TypeScript
│   └── src/app/        # Роуты: /, /aboutme, /ihome, /trade4me, /sdart, /controlpanel
├── docker/              # Dockerfiles + nginx.conf + docker-compose.yml
├── docs/                # Документация
│   ├── ARCHITECTURE.md  # Архитектура и диаграммы
│   ├── DEPLOY.md        # Деплой на VPS
│   └── API.md           # REST API документация
├── SPEC.md              # Техническое задание
└── README.md            # Этот файл
```

## Тесты

```bash
# Все тесты бэкенда (103 теста, >=80% покрытие)
uv run pytest --cov=backend --cov-fail-under=80

# Фронтенд: unit-тесты (Vitest)
cd frontend && npm run test

# Фронтенд: E2E (Playwright)
npm run test:e2e
```

## Деплой

См. `docs/DEPLOY.md` — настройка VPS, Docker Compose, nginx, SSL (Let's Encrypt), резервное копирование.

## Лицензия

Private. Все права защищены.
