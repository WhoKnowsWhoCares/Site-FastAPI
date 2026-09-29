# API Документация — Site-FastAPI

Базовый URL: `http://localhost:8000/api` (dev) или `https://yourdomain.com/api` (prod)

## Аутентификация

Большинство admin-эндпоинтов требуют Bearer токен в заголовке:

```
Authorization: Bearer <jwt_token>
```

Токен получается через OAuth flow и сохраняется как httpOnly cookie на фронтенде.

---

## Authentication (`/auth`)

### Получить OAuth URL авторизации

Получить URL для перенаправления пользователя к провайдеру OAuth.

```
GET /auth/oauth/{provider}/url
```

**Path Parameters:**

| Параметр | Тип | Описание |
|---|---|---|
| `provider` | string | Один из: `github`, `google`, `telegram` |

**Response 200:**

```json
{
  "authorization_url": "https://github.com/login/oauth/authorize?client_id=...&state=...",
  "state": "random_state_string"
}
```

**Response 400:** Неизвестный провайдер.

---

### OAuth Callback

Обработка обратного вызова от OAuth провайдера.

```
POST /auth/oauth/{provider}/callback
```

**Request Body:**

```json
{
  "code": "authorization_code_from_provider",
  "state": "state_parameter"
}
```

**Response 200:**

```json
{
  "access_token": "jwt_token_here",
  "expires_in": 1800
}
```

**Response 400:** Ошибка верификации state или получение user info.

---

### Telegram Callback

Обработка callback от Telegram Login Widget.

```
POST /auth/oauth/telegram/callback
```

**Request Body:** (полный JSON из Telegram auth_data)

```json
{
  "id": 123456789,
  "first_name": "Alexander",
  "last_name": "User",
  "username": "alexuser",
  "photo_url": "https://t.me/...",
  "auth_date": 1727600000,
  "hash": "abc123..."
}
```

**Response 200:** JWT token (как выше).

---

### Получить информацию о текущем пользователе

```
GET /auth/me
```

**Headers:** `Authorization: Bearer <token>`

**Response 200:**

```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "Alexander",
  "avatar_url": "https://avatars.githubusercontent.com/u/123",
  "is_active": true,
  "is_admin": true,
  "created_at": "2026-09-28T10:00:00Z",
  "updated_at": "2026-09-28T10:00:00Z"
}
```

**Response 401:** Не авторизован.

---

### Выход

```
POST /auth/logout
```

**Response 200:**

```json
{
  "message": "Logged out successfully"
}
```

---

### Получить доступные секции контента

```
GET /auth/sections
```

**Response 200:**

```json
["aboutme", "ihome", "trade4me", "sdart"]
```

---

## Public Content (`/content`)

Публичные эндпоинты для чтения контента.

### Получить контент секции

```
GET /content/{section}
```

**Path Parameters:**

| Параметр | Тип | Описание |
|---|---|---|
| `section` | string | `aboutme`, `ihome`, `trade4me`, `sdart` |

**Response 200:**

```json
{
  "section": "aboutme",
  "content": [
    {
      "id": 1,
      "section": "aboutme",
      "content_type": "text",
      "title": "About Me",
      "body": "Developer and analyst...",
      "order": 1,
      "is_published": true,
      "created_at": "2026-09-28T10:00:00Z",
      "updated_at": "2026-09-28T10:00:00Z"
    }
  ],
  "projects": [
    {
      "id": 1,
      "section": "aboutme",
      "title": "Project Alpha",
      "slug": "project-alpha",
      "description": "A cool project",
      "order": 1,
      "is_published": true,
      "created_at": "2026-09-28T10:00:00Z",
      "updated_at": "2026-09-28T10:00:00Z"
    }
  ]
}
```

**Response 404:** Секция не найдена.

---

### Получить конкретный элемент контента

```
GET /content/{section}/{slug}
```

**Path Parameters:**

| Параметр | Тип | Описание |
|---|---|---|
| `section` | string | Название секции |
| `slug` | string | URL-slug элемента (для projects) |

**Response 200:** `{ "type": "content" | "project", ...item_data }`

**Response 404:** Элемент не найден.

---

## Admin (`/admin`)

Все эндпоинты требуют `Authorization: Bearer <token>` с админ-правами.

### Создать контент

```
POST /admin/content
```

**Request Body:**

```json
{
  "section": "aboutme",
  "content_type": "text",
  "title": "New Section",
  "body": "Content body here...",
  "order": 5,
  "is_published": true
}
```

**Response 200:** Созданный ContentRead объект.

**Response 401:** Не авторизован.

---

### Обновить контент

```
PUT /admin/content/{content_id}
```

**Request Body (частичное обновление):**

```json
{
  "title": "Updated Title",
  "body": "Updated body"
}
```

**Response 200:** Обновлённый ContentRead.

**Response 404:** Контент не найден.

---

### Удалить контент

```
DELETE /admin/content/{content_id}
```

**Response 200:** `{"message": "Content deleted successfully"}`

**Response 404:** Контент не найден.

---

### Переместить контент (изменить порядок)

```
POST /admin/content/reorder
```

**Request Body:**

```json
{
  "section": "aboutme",
  "content_orders": [
    {"content_id": 1, "order": 10},
    {"content_id": 2, "order": 5},
    {"content_id": 3, "order": 1}
  ]
}
```

**Response 200:** `{"message": "Content reordered successfully"}`

---

### CRUD Проектов

Аналогичные эндпоинты для проектов:

| Метод | Endpoint | Описание |
|---|---|---|
| `POST` | `/admin/project` | Создать проект |
| `PUT` | `/admin/project/{project_id}` | Обновить проект |
| `DELETE` | `/admin/project/{project_id}` | Удалить проект |

**Request Body (создание):**

```json
{
  "section": "trade4me",
  "title": "Trading Bot",
  "slug": "trading-bot",
  "description": "Automated trading system",
  "order": 1,
  "is_published": true
}
```

---

### Список всего контента (админ)

```
GET /admin/content?page=1&page_size=20&section=aboutme
```

**Query Parameters:**

| Параметр | Тип | По умолчанию | Описание |
|---|---|---|---|
| `page` | int | 1 | Номер страницы (>=1) |
| `page_size` | int | 20 | Размер страницы (1-100) |
| `section` | string | null | Фильтр по секции |

**Response 200:**

```json
{
  "items": [...],
  "total": 42,
  "page": 1,
  "page_size": 20,
  "total_pages": 3
}
```

---

### Список всех проектов (админ)

```
GET /admin/projects?page=1&page_size=20&section=trade4me
```

Аналогично `/admin/content` с пагинацией.

---

## Схемы данных

### ContentRead

```json
{
  "id": 1,
  "section": "aboutme",
  "content_type": "text",
  "title": "Title",
  "body": "Body content...",
  "order": 1,
  "is_published": true,
  "created_at": "2026-09-28T10:00:00Z",
  "updated_at": "2026-09-28T10:00:00Z"
}
```

### ProjectRead

```json
{
  "id": 1,
  "section": "trade4me",
  "title": "Project Name",
  "slug": "project-name",
  "description": "Description...",
  "order": 1,
  "is_published": true,
  "created_at": "2026-09-28T10:00:00Z",
  "updated_at": "2026-09-28T10:00:00Z"
}
```

### UserRead

```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "Alexander",
  "avatar_url": "https://...",
  "is_active": true,
  "is_admin": false,
  "created_at": "2026-09-28T10:00:00Z",
  "updated_at": "2026-09-28T10:00:00Z"
}
```

### Token

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "expires_in": 1800
}
```

---

## Ошибки

Все эндпоинты возвращают стандартные HTTP статус-коды:

| Код | Описание |
|---|---|
| 200 | OK |
| 400 | Bad Request (валидация, OAuth ошибка) |
| 401 | Unauthorized (нет токена или неверный) |
| 403 | Forbidden (нет admin прав) |
| 404 | Not Found |
| 422 | Validation Error (неверный формат запроса) |
| 501 | Not Implemented |

Формат ошибки:

```json
{
  "detail": "Ошибка валидации"
}
```

---

## OpenAPI Spec

Полная спецификация OpenAPI 3.1 доступна по адресу:

- Dev: `http://localhost:8000/openapi.json`
- Docs UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
