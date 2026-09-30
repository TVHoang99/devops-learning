#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

services=("nginx" "ssh")

for service in "${services[@]}"; do

    status=$(systemctl is-active "$service")

    if [ "$status" = "active" ]; then
        echo -e "${GREEN}[OK]${NC} $service active."

    else
        echo -e "${RED}[WARNING]${NC} $service not active! Status: $status"
    fi

done