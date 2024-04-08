## Для запуска проекта понадобится

- Запустить docker compose командой ```docker compose up```
- Зайти внутрь контейнера postgresql ```docker exec -it postgres /bin/bash```
- В случае, если в postgres отсутствуют данные накатить dump ```psql -U app -w 123qwe -d movies_database < /docker-entrypoint-initdb.d/dump.sql```
- В файле .env.example необходимые переменные окружения