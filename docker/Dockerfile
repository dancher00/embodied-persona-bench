FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY pyproject.toml README.md /app/
COPY src /app/src
COPY scripts /app/scripts
COPY tools /app/tools
COPY schema /app/schema
COPY data /app/data
COPY docker/entrypoint.sh /app/docker/entrypoint.sh

RUN chmod +x /app/docker/entrypoint.sh && \
    pip install --upgrade pip && \
    pip install -e ".[annotate,api]"

EXPOSE 8501 8000 8765

ENTRYPOINT ["/app/docker/entrypoint.sh"]
