FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY monitor.py rentvalley.py telegram_notify.py loop_cloud.py ./

ENV DATA_DIR=/data
ENV CHECK_INTERVAL_SEC=600

VOLUME /data

CMD ["python", "-u", "loop_cloud.py"]
