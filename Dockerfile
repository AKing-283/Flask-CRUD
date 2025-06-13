# ✅ Use tag only (recommended for simplicity)
FROM python@sha256:feeffe617f3de614b5efe187bbb57c5a969019b768695b25410be1a8672d11a0

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.main:app"]
