# docker build -t process_a -f process_a.dockerfile .
FROM python:3.7

COPY process_a.py run.py

ENTRYPOINT ["python", "run.py"]
