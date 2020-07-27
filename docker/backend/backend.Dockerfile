FROM python:3.7

# set environment variables
#ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
#ENV DEBUG 0

RUN apt-get update && apt-get install -y default-libmysqlclient-dev build-essential

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
ADD docker/entry.sh /code/docker/entry.sh
RUN chmod gu+x /code/docker/entry.sh
CMD ["./docker/wait-for-mysql.sh", "db", "3306", "womcs_password", "womcs_db", "--", "./docker/entry.sh"]
