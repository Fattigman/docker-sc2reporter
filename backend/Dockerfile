FROM python:3.10-slim-bullseye

# Install needed programs.
RUN apt-get update && \
    apt-get install -y \
        gcc

# Upgrade pip before installing other packages.
RUN python -m pip install --upgrade pip

# Copy only the requirements file and install them all.
COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

# Copy the entire application into an "app" folder, and use that as workdir
# going forward.
COPY ./ /app
WORKDIR /app

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]