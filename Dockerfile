FROM python:3.12

#
WORKDIR /code

#
COPY ./requirement.txt /code/requirnment.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirnment.txt

#
COPY ./app /code/app

#
ENTRYPOINT ["python","app/downloader-utility.py" ]
