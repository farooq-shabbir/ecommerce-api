#!/usr/bin/env bash
set -e
export DJANGO_DEBUG="${DJANGO_DEBUG:-false}"
export DJANGO_ALLOWED_HOSTS="${DJANGO_ALLOWED_HOSTS:-*}"
docker compose -f docker-compose.ec2.yml up -d --build
docker compose -f docker-compose.ec2.yml ps
