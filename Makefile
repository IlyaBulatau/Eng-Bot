DC = docker compose
FILE = docker-compose.dev.yaml

app: # up dev processes
	$(DC) --env-file .env -f $(FILE) up -d

test_db: # up test processes
	$(DC) --env-file .env.test -f $(FILE) up -d

stop: # stop all containers
	docker stop $$(docker ps -q)

delete: # delete all containers
	docker rm $$(docker ps -a -q)

bot_log:
	docker logs bot -f

test: # run tests
	make $(test_db)
	pytest . -s -v
	docker stop $$(docker ps -q)
	docker rm $$(docker ps -a -q)

restart:
	docker restart $$(docker ps -a -q)