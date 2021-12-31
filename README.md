# WWZD

Big data visualisations

## How to start the project

### DEV MODE

```bash
docker-compose up
```

Access the frontend on http://localhost:8080
Access the backend (swagger) on http://localhost:8081

For easier backend development, when rebuilding docker image often, it would be wise to use pip cache since the modules weight much. Do the following:

`docker-compose.yml`

```yaml
Add volume to backend service

- "$HOME/.cache/pip-docker/:/root/.cache/pip"
```

`entrypoint.sh`

```bash
Create the following file in backend directory

#!/bin/bash

pip install --upgrade pip
pip install -r requirements.txt
exec "$@"
```

`Dockerfile`

```Dockerfile
Modify the dockerfile to following

ADD COPY entrypoint.sh .

Remove RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

ADD RUN pip install gdown==4.2.0

ADD ENTRYPOINT ["./entrypoint.sh"]

### PROD MODE

```bash
docker-compose -f docker-compose.prod.yml up
```

Access the frontend on http://localhost:8080
Access the backend from vue on http://localhost:8080/api (swagger not exposed)
