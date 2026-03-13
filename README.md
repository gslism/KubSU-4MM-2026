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

---

# PYTHON

```bash
$ py -m venv .venv

# LINUX/MACOS
$ source .venv/bin/activate 
# WINDOWS
$ .venv\Scripts\activate

$ where python
$ where pip

$ python -m pip install --upgrade pip
$ python main.py
```


# OLLAMA

```bash
$ docker compose -f docker-compose.ollama.yml up -d

$ docker exec -it ollama ollama run deepseek-r1:1.5b
$ docker exec -it ollama ollama run deepseek-r1:7b

$ docker exec -it ollama ollama run qwen2.5:7b
$ docker exec -it ollama ollama run qwen2.5-coder:7b

$ docker compose -f docker-compose.ollama.yml down
```