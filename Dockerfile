FROM python:3.9-slim-buster

WORKDIR /code

ENV PORT 80

COPY requirements.txt /code/requirements.txt

RUN pip3 install -r requirements.txt

COPY . /code

#CMD ["python3", "./roseking/manage.py", "runserver"]
CMD ["python3", "./roseking/manage.py", "runserver"]
