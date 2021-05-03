SHELL := /bin/bash
CURRENT_PATH := $(shell pwd)

build:
	docker-compose up --build -d

run:
	docker-compose up -d
	
destroy:
	docker-compose down