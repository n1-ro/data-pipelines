# Python service image
FROM python:3.12-slim
WORKDIR /app
COPY pipelines/ ./pipelines/
COPY tests/ ./tests/
CMD ["python", "-m", "pipelines"]
