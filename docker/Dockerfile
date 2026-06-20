FROM python:3.11-slim

WORKDIR /app

# Копируем файл с зависимостями
COPY pyproject.toml ./

# Устанавливаем все зависимости (включая pytest)
RUN pip install --no-cache-dir \
    fastapi==0.115.8 \
    uvicorn==0.34.0 \
    sqlalchemy==2.0.37 \
    psycopg-binary==3.2.4 \
    psycopg==3.2.4 \
    pytest==7.4.0 \
    pytest-asyncio==0.25.3 \
    httpx==0.28.1

# Копируем исходный код
COPY src/ ./src/
COPY tests/ ./tests/

# Устанавливаем пакет в режиме разработки (чтобы работали импорты)
RUN pip install -e .

# Создаем пользователя
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

ENV PYTHONPATH="/app:${PYTHONPATH}"

EXPOSE 8118

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8118"]
