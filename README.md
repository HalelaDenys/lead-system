# Lead System

Система складається з двох сервісів:

- `landing_service` приймає ліди по HTTP і публікує їх у Redis Stream
- `core_service` читає ліди з Redis Stream, виконує dedup і зберігає їх у PostgreSQL

## Швидкий старт

### 1. Підготувати `.env`

У репозиторії використовується файл `.env.exapmle`.

Створи локальний `.env`:

```bash
cp .env.exapmle .env
```

### 2. Запустити застосунок

```bash
docker compose up --build -d
```

Після запуску будуть доступні:

- `landing_service`: `http://localhost:8001`
- `core_service`: `http://localhost:8002`
- `Swagger landing_service`: `http://localhost:8001/docs`
- `Swagger core_service`: `http://localhost:8002/docs`

### 3. Створити тестові дані

Після того як контейнери стартували, потрібно виконати:

```bash
docker compose exec landing_api uv run python src/seed_db.py
```

Скрипт створить:

- тестових affiliates
- тестові offers
- записи `active_affiliate:*` у Redis
- JWT токени для запитів до API

Приклад виводу:

```text
=== Seeded Affiliates ===
  id=4ad3f2a7-9428-4593-ad6c-7270470b7a3b  name=WebMaster Alpha
  token: <jwt_token>
```

Тут:

- `id=4ad3f2a7-9428-4593-ad6c-7270470b7a3b` — це `affiliate_id`
- `token: ...` — це і є твій `Bearer token`

Нижче в блоці `Seeded Offers` будуть `offer_id`, які треба використовувати у запиті на створення ліда.

## Як протестувати API

### 1. Відправити лід у `landing_service`

Візьми:

- `affiliate_id` з блоку `Seeded Affiliates`
- `Bearer token` з поля `token`
- `offer_id` з блоку `Seeded Offers`

Приклад запиту:

```bash
curl -X POST "http://localhost:8001/api/v1/landings/lead" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token_from_seed_db>" \
  -d '{
    "name": "John Doe",
    "phone": "+380991112233",
    "country": "UA",
    "offer_id": "<offer_id_from_seed_db>",
    "affiliate_id": "<affiliate_id_from_seed_db>"
  }'
```

Очікувана відповідь:

```json
{
  "status": "accepted"
}
```

### 2. Отримати аналітику з `core_service`

Після відправки ліда можна перевірити, що `core_service` його обробив:

```bash
curl "http://localhost:8002/api/v1/core/leads?date_from=2026-04-01&date_to=2026-04-27&group=date" \
  -H "Authorization: Bearer <token_from_seed_db>"
```

Для цього запиту:

- використовуй той самий `Bearer token`
- токен має належати тому ж affiliate, від імені якого був створений lead

## Корисні команди

Запуск:

```bash
docker compose up --build -d
```

Зупинка з видаленням volume:

```bash
docker compose down -v
```

Повторний seed:

```bash
docker compose exec landing_api uv run python src/seed_db.py
```

## Архітектура

Потік обробки такий:

1. Клієнт відправляє lead у `landing_service`
2. `landing_service` перевіряє токен і `affiliate_id`
3. Lead публікується в Redis Stream
4. `core_service` читає повідомлення з Redis Stream
5. `core_service` перевіряє дублі через Redis
6. `core_service` зберігає lead у PostgreSQL

Інфраструктура:

- `PostgreSQL` для зберігання lead-ів
- `Redis` як broker і для dedup
- `Alembic` для міграцій
- `Docker Compose` для локального запуску

## Сервіси

### `landing_service`

- порт: `8001`
- docs: `http://localhost:8001/docs`
- endpoint: `POST /api/v1/landings/lead`

Призначення:

- прийняти lead по HTTP
- перевірити Bearer token
- перевірити, що `affiliate_id` з body збігається з affiliate з token
- відправити lead у Redis Stream

### `core_service`

- порт: `8002`
- docs: `http://localhost:8002/docs`
- endpoint: `GET /api/v1/core/leads`

Призначення:

- читати повідомлення з Redis Stream
- відкидати дублікати
- зберігати ліди в БД
- віддавати агреговану аналітику

## Конфігурація

Основні змінні:

```env
APP_CONFIG__DB__USER=lead_admin
APP_CONFIG__DB__PASSWORD=lead_admin_password
APP_CONFIG__DB__HOST=postgres_db
APP_CONFIG__DB__PORT=5432
APP_CONFIG__DB__DB=lead_db

APP_CONFIG__REDIS__HOST=redis
APP_CONFIG__REDIS__PORT=6379
APP_CONFIG__REDIS__DB=0

APP_CONFIG__JWT__SECRET_KEY=your_secret
```

`docker compose` очікує, що ці значення будуть доступні з кореневого `.env`.

## Міграції

Міграції автоматично запускає `landing_service` під час старту контейнера.

Якщо треба виконати вручну:

```bash
uv run python -m alembic -c src/alembic.ini upgrade head
```

## Docker

Окремі Dockerfile:

- `src/landing_service/Dockerfile`
- `src/core_service/Dockerfile`

Обидва образи включають:

- код сервісу
- `src/infrastructure`
- `src/shared`
- `src/alembic.ini`
- `src/alembic`
- `src/seed_db.py`
- `.env.exapmle`
