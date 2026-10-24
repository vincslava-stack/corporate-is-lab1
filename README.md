# Corporate IS Lab 1

## Описание проекта

Проект представляет собой мини-информационную систему для учёта сотрудников организации.

Система позволяет хранить сведения о сотрудниках: ФИО, должность и дату приёма на работу. Управление записями выполняется через административную панель Django.

## Используемые технологии

- Python
- Django
- PostgreSQL
- Docker
- Docker Compose
- Git и GitHub

## Запуск проекта

### 1. Клонирование репозитория

```powershell
git clone https://github.com/vincslava-stack/corporate-is-lab1.git
cd corporate-is-lab1
```

### 2. Создание виртуального окружения

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Установка зависимостей

```powershell
python -m pip install -r requirements.txt
```

### 4. Создание файла `.env`

В корне проекта создай `.env` со следующими параметрами:

```dotenv
POSTGRES_DB=corporate_is
POSTGRES_USER=corporate_is
POSTGRES_PASSWORD=corporate_is_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

### 5. Запуск PostgreSQL

```powershell
docker compose up -d
```

### 6. Создание таблиц

```powershell
python manage.py migrate
```

### 7. Создание администратора

```powershell
python manage.py createsuperuser
```

### 8. Запуск Django

```powershell
python manage.py runserver
```

Административная панель: http://127.0.0.1:8000/admin/

## Модель Employee

- `full_name` — ФИО сотрудника.
- `position` — должность.
- `hired_at` — дата приёма на работу.

## Назначение системы

Мини-ИС предназначена для централизованного хранения и управления базовыми сведениями о сотрудниках организации.
