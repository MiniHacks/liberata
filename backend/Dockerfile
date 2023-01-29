FROM mcr.microsoft.com/playwright/python:next-jammy

RUN python3 -m pip install pipenv

WORKDIR /app
COPY Pipfile /app/Pipfile
COPY Pipfile.lock /app/Pipfile.lock
RUN pipenv install --system

COPY . /app

EXPOSE 8000

ENTRYPOINT ["python3", "-m", "backend_server"]
