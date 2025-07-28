# Cities API & o11y-demo

Мини-сервис, вокруг которого строится домашнее задание «o11y».  
Позволяет хранить список городов в PostgreSQL, получать их постранично и искать ближайшие к заданной точке.  
К сервису уже подключены Prometheus-метрики и Swagger-документация.

## Предварительные требования

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Установка и запуск

### 1. Создание файла окружения

Скопируйте содержимое файла `.env.example` в новый файл с названием `.env`.

Для этого можно выполнить в терминале команду:

```bash
cp .env.example .env
```

### 2. Запуск контейнеров

Запустите проект с помощью Docker Compose:

```bash
docker compose up
```

Дождитесь успешного запуска всех контейнеров.

Через ~30 сек сервисы будут готовы:

| Локальный URL | Публичный URL |
|---------------|---------------|
| http://localhost/api/docs	|Swagger UI 
| http://localhost/metrics | Prometheus-метрики приложения
| http://localhost/ui	Web-UI | для генерации нагрузки
| http://localhost:9090	|Prometheus
|http://localhost:3000 |	Grafana (логин/пароль — admin / admin)

## Доступ снаружи (деплой в Yandex Cloud)
Сервис уже развёрнут по белому IP **51.250.88.180**.  
Все URL-ы из таблицы выше работают 1-к-1, достаточно заменить
`localhost` → `51.250.88.180`.

| Локальный URL | Публичный URL |
|---------------|---------------|
| `http://localhost/api/docs` | **http://51.250.88.180/api/docs** |
| `http://localhost/metrics` | **http://51.250.88.180/metrics** |
| `http://localhost:8081/ui` | **http://51.250.88.180:8081/ui** |
| `http://localhost:9090` | **http://51.250.88.180:9090** |
| `http://localhost:3000` | **http://51.250.88.180:3000** |

## 3. Нагрузочный сервис и наблюдаемость

### 3.1  Load-tester

Контейнер `load-tester` — это крохотное FastAPI-приложение, которое «стреляет» по ручке `/city/get/` и сразу же показывает статистику.

| URL              | Что открывается      |
|------------------|----------------------|
| **/ui**          | Web-форма (RPS, Duration) |
| **/start** (POST)| REST-эндпоинт, принимает <br>`rps`, `duration` и запускает тест |

Поля:

| Параметр  | Тип | Описание                          |
|-----------|-----|-----------------------------------|
| `rps`     | int | Запросов в секунду                |
| `duration`| int | Сколько секунд держать нагрузку   |

Пример CLI-запуска на 150 RPS × 60 s:

```bash
curl -X POST -F rps=150 -F duration=60 http://51.250.88.180/start
```

## 4. Мониторинг: Prometheus + Grafana

### 4.1 Метрики, которые уже собираются

- **HTTP**: `http_requests_total`, `http_request_duration_seconds_*`  
- **PostgreSQL**: `pg_stat_database_xact_commit/rollback`  
- **Runtime**: `python_gc_*`, `process_*`, `go_*`  

### 4.2 Панели дашборда *o11y-check*

| Панель          | Запрос (PromQL)                                                                                                |
| --------------- | -------------------------------------------------------------------------------------------------------------- |
| **HTTP RPS**    | `sum(rate(http_requests_total{handler="/city/get/"}[3s]))`                                                     |
| **DB RPS**      | `sum(rate(pg_stat_database_xact_commit[2s]) + rate(pg_stat_database_xact_rollback[2s]))`                       |
| **p99 latency** | `histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{handler="/city/get/"}[2s])) by (le))` |

*Min interval*: **1s**, *refresh*: **1s**.

> **Примечание**: Grafana усредняет точки по времени, поэтому графики могут немного «скруглять» пики.

### 4.3 Алерты

Все алерты настроены и отправляются в Telegram-бота по ссылке: [t.me/alerts_cities](https://t.me/alerts_cities)

1. **HighPostgresRPS**  
   - **Условие**:  
     ```promql
     sum(
       rate(pg_stat_database_xact_commit{datname="postgres"}[30s])
       + rate(pg_stat_database_xact_rollback{datname="postgres"}[30s])
     ) > 100
     ```  
   - **for**: 5s непрерывно *(для отработки нагрузки `duration ≥ 5s`)*  
   - **Описание**: RPS БД выше 100

2. **HighP99Latency**  
   - **Условие**:  
     ```promql
     histogram_quantile(
       0.99,
       sum(
         rate(http_request_duration_seconds_bucket{handler="/city/get/"}[30s])
       ) by (le)
     ) > 0.5
     ```  
   - **for**: 5s непрерывно *(для отработки нагрузки `duration ≥ 5s`)*  
   - **Описание**: p99 latency свыше 500 ms