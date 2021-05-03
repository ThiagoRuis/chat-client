SHELL := /bin/bash
CURRENT_PATH := $(shell pwd)

build:
	docker-compose up
	
destroy:
	docker-compose down