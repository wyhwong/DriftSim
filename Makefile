export DOCKER_BUILDKIT=1

port ?= 8888
args ?=
version ?= devel

build:
	docker-compose build

develop:
	docker-compose -f docker-compose.yml -f docker-compose-dev.yml up -d driftsim

start:
	args=${args} docker-compose up driftsim

jupyter_up:
	port=${port} docker-compose up -d driftsim_jupyter

jupyter_down:
	docker-compose kill driftsim_jupyter

clean:
	docker-compose down --remove-orphans
