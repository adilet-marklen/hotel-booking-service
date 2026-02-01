# **Mini-spec: сервис бронирования отелей**



## **Цель**



Сервис для управления номерами отелей и бронированиями.

HTTP JSON API без авторизации. Данные хранятся в PostgreSQL и не теряются между перезапусками сервиса.

---

## **API**



### **Rooms (номера)**



#### **Создать номер**

**POST** /rooms/create



**Request (JSON):**

```
{
  "description": "Cozy room with sea view",
  "price": 7500
}
```

**Response (201):**

```
{
  "room_id": 1
}
```

**Ошибки:**

- 400 — { "error": "Invalid payload" }


---

#### **Удалить номер и все его брони**

**DELETE** /rooms/{room_id}



**Response (200):**

```
{
  "status": "ok"
}
```

**Ошибки:**

- 404 — { "error": "Room not found" }


---

#### **Получить список номеров**

**GET** /rooms?sort=price|created_at&order=asc|desc



**Параметры запроса:**

- sort — price или created_at (по умолчанию created_at)

- order — asc или desc (по умолчанию asc)




**Response (200):**

```
[
  {
    "room_id": 1,
    "description": "Cozy room with sea view",
    "price": 7500,
    "created_at": "2026-01-13T10:30:00Z"
  }
]
```

**Ошибки:**

- 400 — { "error": "Invalid sort or order" }


---

### **Bookings (бронирования)**



#### **Создать бронь**

**POST** /bookings/create



**Request (JSON):**

```
{
  "room_id": 1,
  "date_start": "2021-12-30",
  "date_end": "2022-01-02"
}
```

**Response (201):**

```
{
  "booking_id": 1444
}
```

**Ошибки:**

- 404 — { "error": "Room not found" }

- 400 — { "error": "Invalid dates" }


---

#### **Удалить бронь**

**DELETE** /bookings/{booking_id}



**Response (200):**

```
{
  "status": "ok"
}
```

**Ошибки:**

- 404 — { "error": "Booking not found" }


---

#### **Получить список броней номера**

**GET** /bookings/list?room_id={room_id}



**Поведение:**

- параметр room_id обязателен

- бронирования сортируются по date_start по возрастанию




**Response (200):**

```
[
  {
    "booking_id": 1444,
    "date_start": "2021-12-30",
    "date_end": "2022-01-02"
  }
]
```

**Ошибки:**

- 400 — { "error": "room_id is required" }

- 404 — { "error": "Room not found" }


---

## **Модель данных**



### **Room**

- id — primary key

- description — текст, не пустой

- price — число, больше 0

- created_at — дата создания




### **Booking**

- id — primary key

- room_id — foreign key → Room (CASCADE)

- date_start — дата начала

- date_end — дата окончания




**Индексы:**

- (room_id, date_start) для быстрого получения списка броней номера


---

## **Формат запросов**

- Все POST-запросы принимают JSON в теле
- Рекомендуемый заголовок: `Content-Type: application/json`

**Пример (создание брони):**

```
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"room_id":24,"date_start":"2021-12-30","date_end":"2022-01-02"}' \
  http://127.0.0.1:8000/bookings/create
```

---

## **Валидации и правила**



### **Rooms**

- description — непустая строка

- price — положительное число




### **Bookings**

- room_id должен существовать

- формат дат — YYYY-MM-DD

- date_end не может быть меньше date_start


---

## **Ошибки и HTTP-коды**

- Формат ошибки:


```
{ "error": "<message>" }
```

- Коды:

    - 200 — успешные GET / DELETE

    - 201 — успешные POST

    - 400 — невалидные данные

    - 404 — сущность не найдена



---

## **Ограничения (осознанные)**

- Нет авторизации

- Нет пагинации

- Нет сложной бизнес-логики

- Проверка пересечения дат бронирования не реализована в основной версии


---

## **Дополнительное усложнение (опционально)**



Реализовать проверку пересечения дат бронирования.

При попытке создать бронь, пересекающуюся с существующей, возвращать:

- 409 — { "error": "Room is not available for selected dates" }

---

## **Запуск (локально)**

```bash
cp .env.example .env
poetry install
poetry run python manage.py migrate
poetry run python manage.py runserver 0.0.0.0:8000
```

---

## **Запуск через Docker Compose**

```bash
cp .env.example .env
docker compose up --build
```

После запуска сервис доступен по адресу:
- http://127.0.0.1:8000/

Файл `.env` не коммитится. Для локального запуска создайте его из шаблона:
```bash
cp .env.example .env
```

---

## **Тесты (Docker Compose)**

```bash
docker compose exec web pytest
```

---

## **Примеры curl**

**Создать номер:**

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"description":"Cozy room with sea view","price":7500}' \
  http://127.0.0.1:8000/rooms/create
```

**Ответ:**

```
{ "room_id": 1 }
```

**Создать бронь:**

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"room_id":1,"date_start":"2021-12-30","date_end":"2022-01-02"}' \
  http://127.0.0.1:8000/bookings/create
```

**Ответ:**

```
{ "booking_id": 1444 }
```

**Список броней номера:**

```bash
curl -X GET "http://127.0.0.1:8000/bookings/list?room_id=1"
```

**Ответ:**

```
[{"booking_id": 1444, "date_start": "2021-12-30", "date_end": "2022-01-02"}]
```

**Ошибка (create booking: невалидные даты):**

```
{ "error": "Invalid dates" }
```

**Ошибка (create booking: room не найден):**

```
{ "error": "Room not found" }
```

**Ошибка (list bookings: room не найден):**

```
{ "error": "Room not found" }
```

---

## **Вопросы и принятые решения**

- Формат данных — JSON (а не form-urlencoded), чтобы соответствовать требованию JSON API.
- Эндпоинт списка броней — `/bookings/list`, как в примерах задания.
- Используются миграции Django для создания таблиц.
