# Use a base image with Python and a slim OS for a smaller footprint.
FROM python:3.11-slim

# Set the working directory inside the container.
WORKDIR /app

# Install system dependencies needed to build the mysqlclient Python package.
# This must run as the root user.
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    libssl-dev \
    pkg-config \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Add a non-root user for security best practices.
RUN useradd -m django

# Copy the requirements file into a temporary directory.
COPY requirements.txt /tmp/requirements.txt

# Install the Python dependencies for all users.
# This ensures gunicorn is available in the global PATH.
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy the rest of the application code into the app directory.
COPY . .

# Copy the entrypoint script and make it executable.
COPY ./entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Change ownership of the app directory to the new user.
RUN chown -R django:django /app

# Switch to the non-root user.
# This must be done AFTER all dependency installations that require root privileges.
USER django

# Collect static files during the image build process.
RUN python manage.py collectstatic --noinput

# Set the entrypoint to the custom script.
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]