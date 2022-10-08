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
3. Запускаем докер
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
3. Запускаем БД
```bash
foo@bar:~$ docker-compose up db
```
4. Создаем пространство
```bash
foo@bar:~$ python -m venv .venv
```
5. Прокидываем миграции
```bash
foo@bar:~$ make upgrade_head
```
6. Запуска самого приложения
```bash
foo@bar:~$ make run
```
## Deploymant Diagram


## C4 diagram 