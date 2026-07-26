FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml README.md LICENSE ./
COPY src ./src
COPY specifications ./specifications
RUN pip install --no-cache-dir .
ENTRYPOINT ["specctl"]
CMD ["validate", "/app/specifications"]
