- remove dangling images:
    - `docker rmi $(docker images --filter "dangling=true" -q --no-trunc) --force`
    - `docker image prune`
    
- set environment variables:
  - `export $(cat .env/*.env)`
  
- run the services:
  - `docker-compose up`
  
- make requirements:
  - `pip installl pip-tools`
  - `pip-compile requiremnts/requirements.in`
  - update a package:
      - `pip-compile --upgrade-package "<package>==<version>" requirements/requirements.in`
- to use the `docker-compose`, create a folder named `.env` in the directory with the `docker-compose.yml` file.
The `.env` folder must contain files: `app.env` and `db.env` with the corresponding environment variables.
  