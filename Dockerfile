FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install uv, the package installer
RUN pip install uv

# Copy the dependency files to the working directory
COPY pyproject.toml uv.lock ./

# Install any needed packages specified in pyproject.toml
RUN uv sync --no-cache

# Copy the rest of the application's code to the working directory
COPY . .

# Ensure the JSON data file is included
COPY mobile_phones_data.json ./

# Expose the port the app runs on (can be overridden by environment)
EXPOSE 8000

# Use PORT environment variable if available, otherwise default to 8000
CMD sh -c "uv run uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"