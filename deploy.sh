#!/bin/bash
git pull
docker build -t docker_marco_06 .
chmod +x start_marco.sh
chmod +x deploy.sh