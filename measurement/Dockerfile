FROM python:3.11-slim
WORKDIR /app
COPY requirements.base.txt ./
RUN pip install --no-cache-dir -r requirements.base.txt
COPY measurement ./measurement
COPY common ./common
ENV PYTHONUNBUFFERED=1
CMD ["python", "-m", "measurement.main"]
