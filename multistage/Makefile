.PHONY: build-dev

build-dev:
	DOCKER_BUILDKIT=1 docker build -t blog_dev --target dev -f Dockerfile ..

services:
	docker-compose -p blog -f docker-compose.services.yml up -d

development: services
	docker-compose -p blog -f docker-compose.base.yml -f docker-compose.dev.yml up

down:
	docker-compose -f docker-compose.services.yml -f docker-compose.dev.yml down