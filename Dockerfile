FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
COPY README.md .
COPY app ./app

RUN pip install --upgrade pip && \
    pip install --no-cache-dir --extra-index-url https://pypi.org/simple .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
