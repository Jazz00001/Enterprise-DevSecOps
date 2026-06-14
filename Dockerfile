# Stage 1: Build Python dependencies
FROM python:3.11-slim AS builder

WORKDIR /app

COPY src/app/requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# Stage 2: Runtime image
FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/usr/local/bin:$PATH"

WORKDIR /app

RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g 10001 -r -s /usr/sbin/nologin appuser

COPY --from=builder /install /usr/local

COPY src/app/ .

RUN python init_db.py && \
    chown -R 10001:10001 /app && \
    chmod -R a=rX /app

USER 10001:10001

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/health')" || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
