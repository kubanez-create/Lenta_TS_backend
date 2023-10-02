FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r /app/requirements.txt --no-cache-dir
COPY foodcast/ /app
CMD ["python3", "manage.py", "runserver", "0:8000"]