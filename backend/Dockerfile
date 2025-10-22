FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .

# Collectstatic step can be added if STATIC_ROOT is configured
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]
