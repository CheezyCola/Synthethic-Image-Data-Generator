#!/bin/sh
uid=$(eval "id -u")
gid=$(eval "id -g")

docker build -f ./docker/Dockerfile -t iras/blenderproc2 .

