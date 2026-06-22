install:
	pip install -r requirements.txt
	cd frontend && npm install

dev:
	./scripts/dev.sh

build:
	docker build -t backend:latest -f Dockerfile.backend .
	docker build -t frontend:latest -f Dockerfile.frontend .

test:
	pytest
	cd frontend && npm test

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

clean:
	docker-compose down --volumes --remove-orphans
	rm -rf backend/__pycache__ frontend/node_modules