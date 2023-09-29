FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r /app/requirements.txt --no-cache-dir
RUN apt-get update && apt-get install -y libsnappy-dev
RUN CPPFLAGS="-I/usr/local/include -L/usr/local/lib" pip install python-snappy
RUN pip install pystore --no-cache-dir
COPY foodcast/ /app
CMD ["python3", "manage.py", "runserver", "0:8000"]