FROM python:3.14

WORKDIR /app

RUN apt update && apt install -y pipx

RUN pipx install poetry

COPY main.py /app/main.py

RUN chmod +x /app/main.py

CMD ["python", "main.py"]