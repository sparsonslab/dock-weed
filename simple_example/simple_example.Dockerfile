# docker build -t simple_example -f simple_example.Dockerfile .
# INTERACTIVE:
# docker run -it simple_example > output.txt
# PIPE:
# cat input.txt | docker run -i simple_example > output.txt


FROM python:3.7

COPY simple_example2.py .

CMD ["python", "./simple_example2.py"]
