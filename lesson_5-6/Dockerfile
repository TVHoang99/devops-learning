FROM python:3.14

WORKDIR /fasiapi

# Install dependencies using poetry
COPY ./pyproject.toml /fasiapi/pyproject.toml
RUN pip install poetry
# RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi
RUN poetry install --no-interaction --no-ansi

COPY ./main.py /fasiapi/main.py

# Run API after starting
COPY ./startup.sh /fasiapi/startup.sh
RUN chmod +x /fasiapi/startup.sh
ENTRYPOINT ["sh","/fasiapi/startup.sh"]