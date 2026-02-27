# KubSU-4MM-2026

Hello, World!

## Postgres & PgAdmin in Docker

```bash
# To run:
docker compose -f postgres.yml up -d

#To stop:
docker compose -f postgres.yml down
```
## Установка браузерного расширения

1. Откройте Google Chrome и перейдите в `chrome://extensions/`.
2. Включите **Режим разработчика**.
3. Нажмите **Загрузить распакованное расширение** и выберите папку `extension`.
4. Нажмите `Отладка страниц service worker` для просмотра логов и отладки расширения.