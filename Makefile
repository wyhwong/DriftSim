export DOCKER_BUILDKIT=1

port ?= 8888
args ?=

build:
	port=${port} docker-compose build

start:
	port=${port} args=${args} docker-compose up driftsim

jupyter_up:
	port=${port} docker-compose up -d driftsim_jupyter

jupyter_down:
	port=${port} docker-compose kill driftsim_jupyter

clean:
	port=${port} docker-compose down --remove-orphans
