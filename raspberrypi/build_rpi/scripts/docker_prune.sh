#/bin/bash
docker builder prune --all
docker system prune -a -f
docker volume prune -a