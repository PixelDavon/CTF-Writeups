FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    firefox-esr \
    wget \
    gnupg \
    curl \
    unzip \
    xvfb \
    libgtk-3-0 \
    libdbus-glib-1-2 \
    libasound2 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxi6 \
    libxtst6 \
    libxrandr2 \
    libxss1 \
    libxinerama1 \
    libgl1 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install geckodriver
ENV GECKODRIVER_VERSION=v0.36.0
RUN wget -q "https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz" \
    && tar -xzf "geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz" -C /usr/local/bin \
    && rm "geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Expose the Flask port
EXPOSE 9999

# Run the app
CMD ["python", "app.py"]