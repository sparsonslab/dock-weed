# # docker build -t process_b -f process_b.dockerfile .
FROM python:3.7

COPY process_b.py .

COPY process_c.py .

LABEL node.process_b="python process_b.py" node.process_c="python process_c.py"
