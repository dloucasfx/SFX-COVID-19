FROM python:3.6-slim
ADD covid.py /
ADD requirements.txt /
RUN pip install -r requirements.txt
CMD [ "python", "./covid.py" ]