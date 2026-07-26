# Deployment

## Local/CI

```bash
pip install .
specctl validate specifications
```

## Container

```bash
docker build -f infra/Dockerfile -t project-spec-compiler .
docker run --rm project-spec-compiler validate /app/specifications
```

The container includes the supplied specifications. Mount a different specification root under `/work` to validate external portfolios.
