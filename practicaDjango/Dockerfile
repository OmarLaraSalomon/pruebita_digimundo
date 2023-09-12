FROM python:3.8

# set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create the /code directory
RUN mkdir /code

# Set work directory
WORKDIR /code

COPY requirements.txt .
# install python dependencies
RUN pip install -r requirements.txt

# Copy the contents of your project to the container
COPY . .

# Agrega esta línea para copiar los archivos estáticos durante la construcción del contenedor


CMD ["gunicorn", "--config", "gunicorn-cfg.py", "core.wsgi"]
