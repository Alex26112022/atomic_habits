FROM python:latest

LABEL authors="Алексей Денисенко"
LABEL org.opencontainers.image.authors="AlexeyDenisenko2703@yandex.ru"

RUN mkdir -p /home/app

ENV HOME=/home/app
ENV APP_HOME=/home/app/web

RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
RUN mkdir $APP_HOME/media
WORKDIR $APP_HOME

ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local'

RUN curl -sSL https://install.python-poetry.org | python3 -

COPY pyproject.toml ./

RUN poetry install --no-interaction --no-ansi

COPY . .

RUN addgroup app
RUN useradd -g app app
RUN chown -R app:app $APP_HOME
USER app

#CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]