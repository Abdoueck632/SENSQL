FROM ubuntu:latest
RUN apt -y update
RUN apt install -y python3
RUN apt install -y python3-pip
RUN pip3 install flask flask_restplus pyparsing
CMD ["python3","./server.py"]
