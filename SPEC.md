# Spec: Site-FastAPI — Персональный сайт

## Objective

Создать персональный сайт-портфолио с FastAPI бэкендом и Next.js фронтендом. Сайт демонстрирует проекты пользователя (AboutMe, iHome, Trade4Me, SD Art) и имеет защищенную админ-панель (ControlPanel) для управления контентом. Аутентификация через OAuth (GitHub, Google, Telegram).

**Target User:** Alexander (analyst-developer) — личный блог/портфолио + админка для контента.

**Success Criteria:**
- Все 5 разделов доступны и отображаются корректно
- OAuth вход работает для GitHub, Google, Telegram
- Админ-панель позволяет CRUD операции для контента разделов
- Сайт собирается в Docker и деплоится на VPS
- API покрыт тестами ≥ 80%
- Фронтенд собирается в standalone режим для продакшена

## Tech Stack

### Backend
- **Python:** 3.13
- **Framework:** FastAPI 0.141+
- **ORM:** SQLAlchemy 2.0 (async) + aiosqlite
- **Auth:** python-jose (JWT), passlib (bcrypt), oauthlib
- **OAuth Providers:** GitHub, Google, Telegram
- **Config:** pydantic-settings + .env
- **Testing:** pytest + httpx
- **Migration:** alembic (для будущих миграций)
- **Env Manager:** uv

### Frontend
- **Framework:** Next.js 14+ (App Router)
- **Language:** TypeScript 5+
- **Styling:** Tailwind CSS
- **State:** React Query / SWR для серверного состояния
- **Forms:** React Hook Form + Zod
- **UI Components:** shadcn/ui или Headless UI
- **Build Output:** standalone для Docker

### Infrastructure
- **Database:** SQLite (dev) → PostgreSQL (prod, позже)
- **Container:** Docker + Docker Compose
- **Reverse Proxy:** nginx (в контейнере)
- **Deploy:** VPS (Docker Compose)

## Commands

```bash
# Backend
cd backend
uv sync                    # Install deps
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
uv run pytest -v --cov=backend --cov-report=term-missing
uv run pytest -v tests/
uv run alembic upgrade head
uv run alembic revision --autogenerate -m "message"

# Frontend
cd frontend
npm install
npm run dev                # Dev server on :3000
npm run build              # Production build (standalone)
npm run lint
npm run type-check
npm run test

# Full Stack (Docker)
docker compose up -d --build
docker compose logs -f
docker compose down
```

## Project Structure

```
Site-FastAPI/
├── backend/
│   ├── .env.example
│   ├── pyproject.toml / uv.lock
│   ├── main.py                    # App entry point
│   ├── config.py                  # Settings via pydantic-settings
│   ├── database.py                # SQLAlchemy async engine/session
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py                # User, OAuthAccount
│   │   ├── content.py             # PageContent, Project, Media
│   │   └── base.py                # Base model with timestamps
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py                # Token, UserRead, OAuthCallback
│   │   ├── content.py             # Content CRUD schemas
│   │   └── common.py              # Pagination, ErrorResponse
│   ├── api/
│   │   ├── __init__.py
│   │   ├── router.py              # Main API router
│   │   ├── deps.py                # Dependencies (db, current_user)
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py            # /auth/* endpoints
│   │       ├── content.py         # /content/* endpoints
│   │       └── admin.py           # /admin/* endpoints (protected)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py        # JWT, password, OAuth logic
│   │   ├── oauth_service.py       # GitHub/Google/Telegram OAuth
│   │   └── content_service.py     # Content CRUD logic
│   ├── utils/
│   │   ├── __init__.py
│   │   └── security.py            # Password hashing, token utils
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py            # pytest fixtures
│   │   ├── test_auth.py
│   │   ├── test_content.py
│   │   └── test_admin.py
│   └── alembic/
│       ├── env.py
│       ├── script.py.mako
│       └── versions/
├── frontend/
│   ├── package.json
│   ├── tsconfig.json
│   ├── next.config.js             # output: 'standalone'
│   ├── tailwind.config.ts
│   ├── .env.example
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx           # Home
│   │   │   ├── aboutme/page.tsx
│   │   │   ├── ihome/page.tsx
│   │   │   ├── trade4me/page.tsx
│   │   │   ├── sdart/page.tsx
│   │   │   ├── controlpanel/
│   │   │   │   ├── layout.tsx     # Protected layout
│   │   │   │   ├── page.tsx       # Dashboard
│   │   │   │   ├── content/page.tsx
│   │   │   │   └── login/page.tsx
│   │   │   ├── api/               # Next.js API routes (proxy to backend)
│   │   │   └── globals.css
│   │   ├── components/
│   │   │   ├── ui/                # shadcn/ui components
│   │   │   ├── layout/            # Header, Footer, Sidebar
│   │   │   ├── content/           # Content blocks
│   │   │   └── admin/             # Admin forms, tables
│   │   ├── lib/
│   │   │   ├── api.ts             # API client (fetch wrapper)
│   │   │   ├── auth.ts            # Auth helpers
│   │   │   └── utils.ts
│   │   ├── hooks/
│   │   │   ├── useAuth.ts
│   │   │   └── useContent.ts
│   │   └── types/
│   │       ├── auth.ts
│   │       └── content.ts
│   ├── public/
│   └── tests/
│       ├── e2e/
│       └── unit/
├── docker/
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   ├── nginx.conf
│   └── docker-compose.yml
├── docs/
│   ├── ARCHITECTURE.md
│   ├── DEPLOY.md
│   └── API.md
├── .gitignore
├── README.md
└── SPEC.md (this file)
```

## Code Style

### Python (Backend)
```python
# Именование: snake_case для функций/переменных, PascalCase для классов
# Type hints везде
async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

# Pydantic модели для схем
class UserRead(BaseModel):
    id: int
    email: str
    name: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
```

### TypeScript (Frontend)
```typescript
// Строгий TS: noImplicitAny, strictNullChecks
// Именование: camelCase, PascalCase для компонентов/типов
interface User {
  id: number;
  email: string;
  name: string;
  isActive: boolean;
  createdAt: string;
}

// API клиент с типами
async function fetchUser(id: number): Promise<User> {
  const res = await api.get(`/users/${id}`);
  return res.json();
}
```

## Testing Strategy

| Level | Backend | Frontend |
|-------|---------|----------|
| Unit | pytest: services, utils, schemas | Vitest: utils, hooks, components |
| Integration | pytest: API endpoints (httpx + test DB) | - |
| E2E | - | Playwright: critical user flows |
| Coverage | ≥ 80% (pytest-cov) | ≥ 70% (vitest coverage) |

**Test DB:** In-memory SQLite для unit/integration тестов.

## Boundaries

**Always:**
- Запускать тесты перед коммитом (`pre-commit` hook)
- Использовать type hints (Python) / strict TS (Frontend)
- Валидировать входные данные через Pydantic/Zod
- Писать тесты для новой бизнес-логики
- Следовать структуре проекта

**Ask First:**
- Изменения схемы БД (миграции)
- Добавление новых внешних зависимостей
- Изменение Docker/Deploy конфигурации
- Архитектурные решения (новые сервисы, паттерны)

**Never:**
- Коммитить секреты (.env, токены, ключи)
- Редактировать vendor/node_modules
- Удалять падающие тесты без фикса
- Хардкодить URL/ключи в коде
- Коммитить большие бинарные файлы

## Success Criteria (Testable)

1. **Backend API:**
   - `GET /api/v1/content/{section}` возвращает контент раздела
   - `POST /api/v1/auth/oauth/{provider}` инициирует OAuth flow
   - `GET /api/v1/admin/content` требует админ права, возвращает список
   - Все эндпоинты покрыты тестами

2. **Frontend:**
   - 5 страниц рендерятся без ошибок (Home, AboutMe, iHome, Trade4Me, SD Art)
   - ControlPanel доступен только после OAuth входа
   - Админ может создавать/редактировать/удалять контент
   - SSR работает для публичных страниц

3. **Docker:**
   - `docker compose up` поднимает backend:8000, frontend:3000, nginx:80
   - Health checks проходят для всех сервисов

4. **Deploy:**
   - Собранные образы запускаются на VPS
   - nginx проксирует /api → backend, /* → frontend

## Open Questions

1. **Контент SD Art** — это галерея изображений? Нужен ли загрузчик файлов?
2. **iHome** — отображает данные из Home Assistant? Нужен ли API прокси?
3. **Trade4Me** — отображает данные трейдинга? Источник данных?
4. **Telegram OAuth** — используем Telegram Login Widget или Bot API?
5. **Изображения/медиа** — храним в БД (base64), на диске, или S3/MinIO?
6. **Миграции** — сразу настраивать alembic или потом?

---

*Spec version: 1.0*  
*Created: 2026-09-28*  
*Status: DRAFT — awaiting approval*