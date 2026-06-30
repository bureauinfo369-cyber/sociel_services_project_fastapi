# Use the official Python 3.9.13 image from the Docker Hub
FROM python:3.9.13

# Install necessary dependencies, including the ODBC driver
RUN apt-get update && apt-get install -y \
    apt-transport-https \
    curl \
    gnupg \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

# Install fontconfig and fonts (including DejaVu for Arabic support)
RUN apt-get update && apt-get install -y \
    fontconfig \
    fonts-dejavu \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

# Verify DejaVu fonts are installed
RUN ls -la /usr/share/fonts/truetype/dejavu/ && \
    echo "DejaVu fonts installed successfully"

# Configure OpenSSL to allow older TLS versions
RUN sed -i 's/MinProtocol = TLSv1.2/MinProtocol = TLSv1.0/' /etc/ssl/openssl.cnf && \
    sed -i 's/CipherString = DEFAULT@SECLEVEL=2/CipherString = DEFAULT@SECLEVEL=1/' /etc/ssl/openssl.cnf
# Update package lists and install xdg-utils
RUN apt-get update && apt-get install -y xdg-utils
# Set the working directory in the container
WORKDIR /app

# Upgrade pip to a specific version
RUN pip install --upgrade pip==25.3

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Expose the port FastAPI is running on
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]