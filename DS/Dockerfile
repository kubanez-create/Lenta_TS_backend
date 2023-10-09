FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r /app/requirements.txt --no-cache-dir
COPY . /app
CMD ["nohup", "python3", "scheduler.py"]