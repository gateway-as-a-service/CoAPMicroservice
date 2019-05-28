# Our base image
FROM python:3-onbuild

ENV APP_ENV=docker

EXPOSE 5683

# Run application
CMD ["python", "./main.py"]