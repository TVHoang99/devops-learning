#! /bin/bash

# Load configurations with fallback defaults
ENVIRONMENT="${ENVIRONMENT:-local}"
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8000}"
RELOAD="${RELOAD:-true}"
CERTBOT_ENABLED="${CERTBOT_ENABLED:-false}"

CERT_DIR="/fasiapi/certs"
KEY_FILE="${SSL_KEYFILE:-$CERT_DIR/key.pem}"
CERT_FILE="${SSL_CERTFILE:-$CERT_DIR/cert.pem}"

# On Production: Obtain Let's Encrypt certificate if enabled and missing
if [ "$CERTBOT_ENABLED" = "true" ] && [ -n "$DOMAIN" ] && [ -n "$EMAIL" ]; then
    if [ ! -f "$KEY_FILE" ] || [ ! -f "$CERT_FILE" ]; then
        echo "Obtaining Let's Encrypt certificate for $DOMAIN via Certbot..."
        certbot certonly --standalone -d "$DOMAIN" --email "$EMAIL" --agree-tos --non-interactive
    fi
fi

# Fallback: If certificate files do not exist, generate self-signed certificate
if [ ! -f "$KEY_FILE" ] || [ ! -f "$CERT_FILE" ]; then
    echo "Certificate files not found at $CERT_FILE and $KEY_FILE."
    echo "Generating self-signed certificate as fallback..."
    mkdir -p "$(dirname "$KEY_FILE")" "$(dirname "$CERT_FILE")"
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout "$KEY_FILE" \
        -out "$CERT_FILE" \
        -subj "/C=VN/ST=Hanoi/L=Hanoi/O=DevOpsLearning/CN=localhost"
fi

# Configure Uvicorn reload option
UVICORN_RELOAD_OPT=()
if [ "$RELOAD" = "true" ]; then
    UVICORN_RELOAD_OPT+=(--reload)
fi

echo "Starting Uvicorn Server:"
echo " - Environment : $ENVIRONMENT"
echo " - Host        : $HOST"
echo " - Port        : $PORT"
echo " - Reload      : $RELOAD"
echo " - SSL Key     : $KEY_FILE"
echo " - SSL Cert    : $CERT_FILE"

exec poetry run uvicorn main:app "${UVICORN_RELOAD_OPT[@]}" --host "$HOST" --port "$PORT" \
    --ssl-keyfile "$KEY_FILE" \
    --ssl-certfile "$CERT_FILE"