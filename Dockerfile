FROM ubuntu:latest
LABEL authors="uijong"

ENTRYPOINT ["top", "-b"]