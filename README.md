# Backend сервис VTB-00

## Стэк:
    FastAPI + Postgresql
## Как развернуть:
###   из докера весь сервис:
1. Клонируем
```bash
foo@bar:~$ git clone https://github.com/Donut-Panik/Backend
```
2. Заходим в папку
```bash
foo@bar:~$ cd Backend
```
3. Настройте файл settings для s3 хранилища яндекса
```bash
    foo@bar:~$ vim app/endpoints/settings.py
    S3_ENDPOINT_URL = "https://storage.yandexcloud.net"
    S3_AWS_ACCESS_KEY_ID = $KEYID
    S3_AWS_SECRET_ACCESS_KEY = $KEY
    BUCKET_NAME = $NAME
    REGION_NAME = $REGION
```
4. Запускаем докер
```bash
foo@bar:~$ docker-compose up
```
###  Для дальнейшей доработки
1. Клонируем
```bash
foo@bar:~$ git clone https://github.com/Donut-Panik/Backend
```
2. Заходим в папку
```bash
foo@bar:~$ cd Backend
```
3. Настройте файл settings для s3 хранилища яндекс
```bash
    foo@bar:~$ vim app/endpoints/settings.py
    S3_ENDPOINT_URL = "https://storage.yandexcloud.net"
    S3_AWS_ACCESS_KEY_ID = $KEYID
    S3_AWS_SECRET_ACCESS_KEY = $KEY
    BUCKET_NAME = $NAME
    REGION_NAME = $REGION
```
4. Запускаем БД
```bash
foo@bar:~$ docker-compose up db
```
5. Создаем пространство
```bash
foo@bar:~$ python -m venv .venv
```
6. Прокидываем миграции
```bash
foo@bar:~$ make upgrade_head
```
7. Запуска самого приложения
```bash
foo@bar:~$ make run
```
## Deploymant Diagram
![Deployment](https://github.com/Donut-Panik/Backend/blob/main/photo/Deployment.png)

## C4 diagram 
![C4](https://github.com/Donut-Panik/Backend/blob/main/photo/c4.png)
## DB scheme
![DB](https://github.com/Donut-Panik/Backend/blob/main/photo/schema.png)
## Swagger развернуто Backend на сервере
http://92.63.102.121/swagger#/
