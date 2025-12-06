FROM python:3.12.0-slim-bookworm

# Environment variables
ENV PYTHONBUFFERED=1 \
    PYTHONWRITEBYTECODE=1 \
    APP=/app

# Set workdir
WORKDIR $APP

# Install dependencies
COPY requirements.txt $APP
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy project files (including db.sqlite3 if present)
COPY . $APP

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

# Expose port
EXPOSE 8000

# Entrypoint script runs migrations, collectstatic, and starts Gunicorn
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]
