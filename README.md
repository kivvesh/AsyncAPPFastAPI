# etl + AsyncAPI + tests


### Перед разворачиванием и запуском приложения необходимо сделать следующее:
- Перенести переменные окружения из .env.example в .env в следующих директориях:
    - ./.env.example
    - ./src/.env.example
    - ./etl/.env.example
- Запустить `docker compose up` в консоли, находясь в корневой директории проекта
- Заполнить базу данных Postgres данными, загрузив dump: ```docker exec -it postgres_bd /bin/bash``` и ```psql -U app -w 123qwe -d movies_database < /datapsqldump.sql```
- Документация приложения располагается по адресу ```http://localhost:8000/api/openapi``` и доступна после запуска приложения
