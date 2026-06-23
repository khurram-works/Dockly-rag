FROM python:3.13.7-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install torch==2.12.0 --index-url https://download.pytorch.org/whl/cpu
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]