FROM python:3.7

COPY add.py subtract.py ./

LABEL process.python_add="python add.py" process.python_subtract="python subtract.py"
