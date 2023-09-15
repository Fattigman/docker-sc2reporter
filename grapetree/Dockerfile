FROM python:3.7-slim-bullseye

# Install dependencies
COPY . /app
WORKDIR /app

# Install needed programs.
RUN apt-get update && \
    apt-get install -y \
        gcc

RUN pip3 install . && \
    pip3 install pandas requests gunicorn

# Run grapetree
CMD ["gunicorn", "-b", ":4000", "wsgi:application"]