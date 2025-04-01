FROM --platform=linux/amd64 tiangolo/uvicorn-gunicorn-fastapi:python3.7

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install -U -r /app/requirements.txt

# Copy the application code
COPY . /app
WORKDIR /app

# Run the application
CMD ["python", "main.py"]
