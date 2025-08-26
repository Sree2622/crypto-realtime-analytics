# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies (example with kafka-python)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Copy the entrypoint script and make it executable
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Set default command to the entrypoint script
CMD ["./entrypoint.sh"]
