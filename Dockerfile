FROM python:3.11-slim

WORKDIR /app

# Сначала копируем только requirements.txt для кэширования
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Затем копируем остальные файлы
COPY . .

CMD ["python", "bot.py"]