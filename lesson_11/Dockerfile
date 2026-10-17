FROM python:3.14

WORKDIR /fasiapi

# Install dependencies using poetry
COPY ./pyproject.toml /fasiapi/pyproject.toml
RUN pip install poetry
RUN poetry install

COPY ./main.py /fasiapi/main.py

CMD ["poetry", "run", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]

# aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.<region>.amazonaws.com
