FROM python:3.11-slim
WORKDIR /app
COPY ui-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ui-service .
EXPOSE 8000
CMD ["gunicorn", "horilla_ui.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2", "--reload"]
