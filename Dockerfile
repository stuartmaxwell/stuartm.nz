FROM python:3.12-slim-bookworm

RUN apt-get update \
  && apt-get upgrade -y \
  && apt-get install -y build-essential libpq-dev --no-install-recommends \
  && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
  && apt-get clean

# install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# - Silence uv complaining about not being able to use hard links,
# - tell uv to byte-compile packages for faster application startups,
# - prevent uv from accidentally downloading isolated Python builds,
# - pick a Python,
# - and finally declare `/venv` as the target for `uv sync`.
ENV UV_LINK_MODE=copy \
  UV_COMPILE_BYTECODE=1 \
  UV_PYTHON_DOWNLOADS=never \
  UV_PYTHON=python3.12
# UV_PROJECT_ENVIRONMENT=/venv
# UV_CACHE_DIR=/cache

# Set up the environment
COPY pyproject.toml /app/
COPY uv.lock /app/
WORKDIR /app
RUN uv sync --locked --no-dev
COPY . /app
RUN mkdir /app/staticfiles

# Switching to a non-root user
RUN useradd appuser && chown -R appuser /app
USER appuser

EXPOSE 8000
