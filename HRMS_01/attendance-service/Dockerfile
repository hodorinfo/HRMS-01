FROM python:3.11-slim
WORKDIR /app
COPY common-lib /common-lib
RUN pip install --no-cache-dir /common-lib
COPY attendance-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY attendance-service .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
