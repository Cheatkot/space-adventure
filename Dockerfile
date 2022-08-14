FROM python:3.9-slim-buster

WORKDIR /code

ENV PORT 80

COPY requirements.txt /code/requirements.txt

RUN pip3 install -r requirements.txt

COPY . /code

CMD ["docker", "run", "-p", "6379:6379", "-d", "redis:5"]
CMD ["python3", "./roseking/manage.py", "runserver"]
