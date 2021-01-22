FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/flask_bi_report_system

COPY requirements.txt /usr/src/flask_bi_report_system/requirements.txt
RUN pip install -r /usr/src/flask_bi_report_system/requirements.txt

COPY . /usr/src/flask_bi_report_system

EXPOSE 8000
CMD ["python", "report_system.py"]