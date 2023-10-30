DC = docker compose
FILE = docker-compose.dev.yaml

db: # up dev database
	$(DC) --env-file .env -f $(FILE) up -d

test_db: # up test database
	$(DC) --env-file .env.test -f $(FILE) up -d

stop: # stop all containers
	docker stop $$(docker ps -q)

delete: # delete all containers
	docker rm $$(docker ps -a -q)

test: # run tests
	make $(test_db)
	pytest . -s -v
	docker stop $$(docker ps -q)
	docker rm $$(docker ps -a -q)