FROM python:3.12.2-slim as development_build

ARG APP_DIR=/app

ARG ENV

ENV ENV=${ENV} \
    PYTHOPNUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.3.1 \
    UVICORN_PORT=8000   \
    UVICORN_HOST=0.0.0.0 \
    UVICORN_RELOAD=0

# Deploy application
WORKDIR $APP_DIR
COPY pyproject.toml poetry.lock README.md ${APP_DIR}/
ADD models ${APP_DIR}/models
ADD src ${APP_DIR}/src


# System dependencies
RUN pip install --disable-pip-version-check "poetry==$POETRY_VERSION"

# Project initialization:
RUN poetry config virtualenvs.create false \
    && poetry install --only main \
    && poetry run spacy download es_core_news_lg

CMD ["poetry", "run", "python","-m", "plagiarism.main"]