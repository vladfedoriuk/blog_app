- remove dangling images:
    - `docker rmi $(docker images --filter "dangling=true" -q --no-trunc) --force`
    - `docker image prune`
    
- set environment variables:
  - `export $(cat .env/*.env)`
  
- run the services:
  - `docker-compose up`
  
- make requirements:
  - `pip installl pip-tools`
  - `pip-compile requiremnts/requiremnts.in`
  - update a package:
      - `pip-compile --upgrade-package "<package>==<version>" requirements/requirements.in`
  