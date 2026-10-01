FROM python:3.14

WORKDIR /fasiapi

# Install dependencies using poetry
COPY ./pyproject.toml /fasiapi/pyproject.toml
RUN pip install poetry
RUN poetry install

# Generate self-signed SSL/TLS certificate
RUN mkdir -p /fasiapi/certs && \
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout /fasiapi/certs/key.pem \
        -out /fasiapi/certs/cert.pem \
        -subj "/C=VN/ST=Hanoi/L=Hanoi/O=DevOpsLearning/CN=localhost"

COPY ./main.py /fasiapi/main.py

# Run API after starting
COPY ./startup.sh /fasiapi/startup.sh
RUN chmod +x /fasiapi/startup.sh
ENTRYPOINT ["/fasiapi/startup.sh"]