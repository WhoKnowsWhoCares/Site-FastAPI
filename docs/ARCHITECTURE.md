# Архитектура проекта Site-FastAPI

## Обзор системы

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│   Browser   │────▶│    Nginx     │────▶│  Next.js     │
│  (Client)   │◀────│  :80 (SSL)   │◀────│  Frontend    │
└─────────────┘     │              │     │  :3000       │
                    │  /api/ ────▶ │────▶│  FastAPI     │
                    │              │     │  Backend     │
                    └──────────────┘     │  :8000       │
                                         └──────┬───────┘
                                                │
                                         ┌──────▼───────┐
                                         │   SQLite /   │
                                         │  PostgreSQL  │
                                         └──────────────┘
```

## Компоненты

### Бэкенд (FastAPI)

```
backend/
├── main.py              # Async lifespan, app factory, uvicorn entry
├── config.py            # pydantic-settings Settings
├── database.py          # SQLAlchemy async engine + session factory
├── api/
│   ├── router.py        # Mount all v1 routers under /api
│   ├── deps.py          # Dependencies: get_db, get_current_user, get_current_admin
│   └── v1/
│       ├── auth.py      # OAuth URLs, callback, /me, logout, sections
│       ├── content.py   # Public GET /content/{section}[/{slug}]
│       └── admin.py     # Protected CRUD + reorder (Bearer ADMIN_TOKEN)
├── services/
│   ├── auth_service.py  # JWT create/verify, password hash, user management
│   ├── oauth_service.py # GitHub/Google/Telegram OAuth flows
│   └── content_service.py # CRUD for PageContent, Project, Media
├── models/
│   ├── base.py          # Base model with timestamps
│   ├── user.py          # User + OAuthAccount
│   └── content.py       # PageContent + Project + Media
├── schemas/
│   ├── auth.py          # Token, UserRead, OAuthCallback, OAuthUrlResponse
│   ├── content.py       # ContentCreate/Update/Read, Project*, MediaRead
│   └── common.py        # PaginationParams, ErrorResponse
└── utils/
    └── security.py      # JWT token utils, password hashing
```

### Фронтенд (Next.js)

```
frontend/src/
├── app/
│   ├── layout.tsx       # Root layout with AuthProvider + Header/Footer
│   ├── page.tsx         # Home — grid of content sections
│   ├── aboutme/page.tsx # AboutMe section page
│   ├── ihome/page.tsx   # iHome section page
│   ├── trade4me/page.tsx # Trade4Me section page
│   ├── sdart/page.tsx   # SD Art section page
│   └── controlpanel/    # Admin dashboard (protected)
│       ├── login/page.tsx      # OAuth login buttons
│       ├── callback/oauth-callback-inner.tsx  # OAuth callback handler
│       ├── (dashboard)/page.tsx          # Dashboard stats
│       └── (dashboard)/content/page.tsx    # Content CRUD table
├── components/
│   ├── ui/              # shadcn/ui primitives (Button, Dialog, Table...)
│   ├── layout/          # Header, Footer, SectionCard, OAuthLoginButtons
│   ├── admin/           # AdminSidebar, ContentTable, ContentForm, ConfirmDialog
│   └── content/         # SectionPage (SSR content rendering)
├── hooks/
│   ├── useAuth.tsx      # Auth context, login/logout, token management
│   └── useContent.ts    # React Query hooks for content CRUD
├── lib/
│   ├── api.ts           # Fetch wrapper with auth header
│   ├── auth.ts          # OAuth helpers, cookie handling
│   ├── content.ts       # Content section config
│   ├── validations.ts   # Zod schemas (contentFormSchema)
│   └── utils.ts         # Shared utilities
├── types/
│   ├── auth.ts          # User, Token, OAuthProvider types
│   └── content.ts       # ContentSection, PageContent, Project types
└── middleware.ts        # Client-side auth guard for /controlpanel
```

## Поток данных

### Публичная страница (SSR)

```
Browser → Nginx → Next.js SSR → API client (fetch) → FastAPI /api/content/{section}
                                                          ↓
                                                   ContentService.get_section_data()
                                                          ↓
                                                   SQLAlchemy query → SQLite
```

1. Пользователь открывает `/aboutme`
2. Next.js SSR вызывает `getServerSideProps` (или server component fetch)
3. API client делает GET к FastAPI endpoint `/api/content/aboutme`
4. ContentService извлекает данные из БД
5. Next.js рендерит HTML и отправляет клиенту

### Админ-панель (CSR + OAuth)

```
Browser → Nginx → Next.js CSR → Middleware auth guard
                                    ↓ (no token)
                              /controlpanel/login
                                    ↓ (click GitHub)
                         FastAPI /api/auth/oauth/github/url
                                    ↓
                         Browser → GitHub OAuth consent
                                    ↓ (callback)
                         FastAPI /api/auth/oauth/github/callback
                                    ↓ (JWT in httpOnly cookie)
                         Redirect → /controlpanel
```

1. Пользователь заходит на `/controlpanel`
2. Middleware проверяет наличие JWT в httpOnly cookie
3. Если нет — редирект на `/controlpanel/login`
4. Клик по кнопке OAuth → GET к FastAPI для получения URL авторизации
5. Пользователь авторизуется у провайдера
6. Callback → FastAPI создаёт JWT → httpOnly cookie → redirect на dashboard
7. Dashboard загружает контент через React Query hooks

### CRUD операции (Admin)

```
Browser → POST /api/admin/content {section, content_type, title, body}
          Headers: Authorization: Bearer <token>
                                    ↓
                         get_current_admin dependency
                                    ↓
                         ContentService.create_content()
                                    ↓
                         SQLAlchemy INSERT → SQLite
```

## Аутентификация

### JWT Flow

1. **Создание токена:** `auth_service.create_token(user)` → python-jose HS256
   - subject = user.id (str)
   - email, is_admin claims
   - expires_in = 30 минут (настраиваемо)

2. **Проверка токена:** `auth_service.get_current_user(token)`
   - Декодирует JWT через jose
   - Находит пользователя в БД по id
   - Возвращает User объект или None

3. **Admin доступ:** `get_current_admin(current_user)`
   - Проверяет current_user.is_admin == True
   - Возвращает dict с данными админа

### OAuth Flow (GitHub/Google)

1. Frontend GET `/api/auth/oauth/{provider}/url`
2. Backend генерирует state, сохраняет mapping state→provider
3. Возвращает authorization_url + state
4. Пользователь авторизуется у провайдера
5. Callback на FastAPI с code + state
6. Верификация state (consume-once)
7. Exchange code → access_token → user_info
8. Find or create User in DB
9. Create JWT → httpOnly cookie

### Telegram Login Widget

Альтернативный flow: widget отправляет auth_data POST на бэкенд, который верифицирует hash через HMAC-SHA256 с bot token.

## Безопасность

| Мера | Реализация |
|---|---|
| Пароли | bcrypt (passlib) — хеширование при создании |
| Токены | JWT HS256, httpOnly cookie, 30min TTL |
| Admin | `get_current_admin` dependency — проверка is_admin flag |
| CORS | Настроен через FastAPI CORSMiddleware |
| Валидация | Pydantic schemas (backend) + Zod (frontend) |

## База данных

- **Dev:** SQLite via aiosqlite (`sqlite+aiosqlite:///./site.db`)
- **Prod:** PostgreSQL (переключение через DATABASE_URL)
- **ORM:** SQLAlchemy 2.0 async с sessionmaker
- **Миграции:** Alembic (initial migration для User, OAuthAccount, PageContent, Project, Media)

### Таблицы

| Таблица | Назначение |
|---|---|
| `users` | Пользователи: email, name, hashed_password, is_admin, avatar_url |
| `oauth_accounts` | Связь User ↔ OAuth provider (provider, provider_user_id, access_token) |
| `page_content` | Контент секций: section, content_type, title, body, order, is_published |
| `projects` | Проекты: section, title, slug, description, order, is_published |
| `media` | Медиафайлы: section, file_url, file_type, alt_text |
