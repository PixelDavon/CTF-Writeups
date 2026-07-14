#!/bin/bash
docker stop leaks || true
docker rm leaks || true
docker build -t leaks .
docker run -dit -p9999:9999 --name leaks leaks