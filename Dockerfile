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

# Expose the port the app runs on
EXPOSE 8000

CMD ["uv", "run", "run.py"]