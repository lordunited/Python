FROM python:3.9
RUN pip install cx_Oracle==8.3.0 Requests==2.31.0 
RUN mkdir /opt/oracle && cd /opt/oracle
WORKDIR /opt/oracle
COPY watcher-agent.py .
RUN wget https://download.oracle.com/otn_software/linux/instantclient/214000/instantclient-basic-linux.x64-21.4.0.0.0dbru.zip
RUN unzip instantclient-basic-linux.x64-21.4.0.0.0dbru.zip 
RUN apt update && apt install libaio1 
RUN  echo /opt/oracle/instantclient_21_4 > /etc/ld.so.conf.d/oracle-instantclient.conf && \
    ldconfig
CMD ["python","watcher-agent.py"]

