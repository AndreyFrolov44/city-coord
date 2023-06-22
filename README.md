# Сервис получения координат

## Технологии
 - Python
 - FastApi
 - PostgreSQL/PostGIS

## API
Для получения координат городов используется OpenStreetMap

1. POST /api/cities/create

Добавление в базу данных нового города. Если найдено несколько городов с одинаковым названием, то будут добавлены все.

#### Параметры запроса
|Параметр|Тип|Описание|
|--------|---|--------|
|city_name|string|Название города|


#### Пример запроса
```
curl -X 'POST' \
  'http://localhost:8000/api/cities/create?city_name=Lipetsk' \
  -H 'accept: application/json' \
  -d ''
```

#### Пример ответа
```json
[
  {
    "name": "Lipetsk, Lipetsk Oblast, Central Federal District, 398000, Russia",
    "lat": 52.6041877,
    "lon": 39.5936899
  }
]
```

2. DELETE /api/cities/delete

Удаление города по имени

#### Параметры запроса
|Параметр|Тип|Описание|
|--------|---|--------|
|city_name|string|Название города|


#### Пример запроса
```
curl -X 'DELETE' \
  'http://localhost:8000/api/cities/delete?city_name=Lipetsk%2C%20Lipetsk%20Oblast%2C%20Central%20Federal%20District%2C%20398000%2C%20Russia' \
  -H 'accept: application/json'
```

3. GET /api/cities

Получение информации о городе.

#### Параметры запроса
|Параметр|Тип|Описание|
|--------|---|--------|
|city_name|string|Название города|


#### Пример запроса
```
curl -X 'GET' \
  'http://localhost:8000/api/cities?city_name=Lipetsk%2C%20Lipetsk%20Oblast%2C%20Central%20Federal%20District%2C%20398000%2C%20Russia' \
  -H 'accept: application/json'
```

#### Пример ответа
```json
{
  "name": "Lipetsk, Lipetsk Oblast, Central Federal District, 398000, Russia",
  "lat": 52.6041877,
  "lon": 39.5936899
}
```

4. GET /api/cities/nearest

Получение двух ближайших соседей для заданной точки

#### Параметры запроса
|Параметр|Тип|Описание|
|--------|---|--------|
|lat|float|Широта|
|lon|float|Долгота|


#### Пример запроса
```
curl -X 'GET' \
  'http://localhost:8000/api/cities/nearest?lat=42.732344&lon=12.437154' \
  -H 'accept: application/json'
```

#### Пример ответа
```json
[
  {
    "name": "Rome, Roma Capitale, Lazio, Italy",
    "lat": 41.8933203,
    "lon": 12.4829321,
    "distance": 93371.20803817
  },
  {
    "name": "City of San Marino, 47890, San Marino",
    "lat": 43.9363996,
    "lon": 12.4466991,
    "distance": 133887.28384642
  }
]
```

## Запуск
**Перед запуском необходимо заполнить файл ```.env```**
```text
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=
POSTGRES_PORT=
```

Для запуска ввести команду:
```shell
docker-compose up -d --build
```

Для запуска тестов ввести команду:
```shell
docker exec api-cdn pytest
```
