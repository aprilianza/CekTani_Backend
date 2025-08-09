# Gunakan Python image resmi
FROM python:3.11-slim

# Set workdir di container
WORKDIR /app


# Copy requirements.txt
COPY requirements.txt .

# Install dependencies Python
RUN pip install --no-cache-dir -r requirements.txt

# Copy semua file project ke container
COPY . .

# Expose port FastAPI
EXPOSE 8000

# Jalankan server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
