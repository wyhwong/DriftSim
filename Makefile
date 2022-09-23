export DOCKER_BUILDKIT=1

build:
	docker build -t driftsim .

start:
	args=${args} docker-compose up

clean:
	docker-compose down --remove-orphans
