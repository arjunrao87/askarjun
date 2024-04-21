build: 
	docker build -t askarjun .

tag: 
	docker tag askarjun ghcr.io/arjunrao87/askarjun:0.1

build-image: build tag

up:
	docker-compose up