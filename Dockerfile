
#Python runtime for parent image
FROM python:3.9-slim


WORKDIR /app

#python dependencies 
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

# Expose the port your Flask app will run on
EXPOSE 6000

# Set env vars for Flask, localhost 6000
ENV FLASK_APP=backend.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=6000

# run flask server
CMD ["flask", "run"]
