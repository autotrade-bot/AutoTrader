FROM python:3.6.4-jessie

RUN apt update && apt install -y mariadb-client
COPY ./ /mnt/
RUN cd /mnt \
&& pip install -r requirements.txt \
&& python setup.py install
