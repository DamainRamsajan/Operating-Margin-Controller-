# Production image for the OMC console (reference). Build: docker build -t omc:0.1 .
# Pin the base image by digest in CI (docker pull python:3.12-slim-bookworm; use the digest it prints).
FROM python:3.12-slim-bookworm AS build
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 PIP_NO_CACHE_DIR=1
WORKDIR /src
COPY requirements/runtime.txt requirements/runtime.txt
RUN python -m venv /opt/venv && /opt/venv/bin/pip install --require-hashes -r requirements/runtime.txt
COPY pyproject.toml README.md ./
COPY src ./src
RUN /opt/venv/bin/pip install --no-deps .

FROM python:3.12-slim-bookworm
ENV PATH="/opt/venv/bin:$PATH" PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 OMC_AUTH_MODE=proxy
COPY --from=build /opt/venv /opt/venv
RUN useradd --system --uid 10001 --no-create-home --shell /usr/sbin/nologin omc && mkdir /data && chown omc:omc /data
USER 10001
WORKDIR /data
VOLUME ["/data"]
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/healthz', timeout=2).status == 200 else 1)"
# The container refuses to start without OMC_PROXY_SECRET (shared with your authenticating proxy).
ENTRYPOINT ["omc", "console", "--workspace", "/data", "--host", "0.0.0.0", "--port", "8000", "--auth-mode", "proxy", "--hsts"]
