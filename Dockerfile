FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY joke_mcp_server.py .

EXPOSE 2009

CMD ["python", "joke_mcp_server.py"]
