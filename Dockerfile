FROM python:latest

# Update package lists and install necessary dependencies
RUN apt-get update && \
    apt-get install -y build-essential


# Set environment variables (e.g., set Python to run in unbuffered mode)
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy your application's requirements and install them
COPY requirements.txt /app/

RUN export HNSWLIB_NO_NATIVE=1  
RUN pip install -r /app/requirements.txt

# Copy your application code into the container
COPY . /app/

EXPOSE 8080

CMD ["python", "-m", "chainlit", "run", "src/chat.py", "-h", "--port", "8080"]