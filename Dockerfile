FROM python:3.11-slim AS builder

WORKDIR /app

COPY src/app/requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/usr/local/bin:$PATH"

WORKDIR /app

RUN groupadd -r appgroup && \
    useradd -r -g appgroup -u 10001 appuser

COPY --from=builder /install /usr/local

COPY src/app/ .

RUN python init_db.py && \
    chown -R appuser:appgroup /app

USER appuser

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/health')" || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
