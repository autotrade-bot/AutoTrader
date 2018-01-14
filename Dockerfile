FROM python:3.6.4-jessie

COPY ./ /mnt/
RUN cd /mnt \
&& pip install -r requirements.txt \
&& python setup.py install

ENTRYPOINT cd /mnt/autotrade && while true; do python worker.py; sleep 60; done;
