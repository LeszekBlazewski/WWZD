# WWZD

Big data visualisations

## Docker INFO

All of the loaded models/datasets are really memory hungry, so be sure to give your docker resources around 14GB.

## How to start the project

### DEV MODE

```bash
docker-compose up
```

Access the frontend on http://localhost:8080
Access the backend (swagger) on http://localhost:8081

For easier backend development, when rebuilding docker image often, it would be wise to use pip cache since the modules weight much. Do the following:

Change the line with pip install in `Dockerfile` to:

```Dockerfile
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
```

```bash
docker-compose up
```

If the command files it might be necessary to:

1. Add the line `# syntax = docker/dockerfile:experimental` as first line in Dockerfile
2. Run `export DOCKER_BUILDKIT=1` before issuing `docker-compose up` 
### PROD MODE

```bash
docker-compose -f docker-compose.prod.yml up
```

Access the frontend on http://localhost:8080
Access the backend from vue on http://localhost:8080/api (swagger not exposed)
