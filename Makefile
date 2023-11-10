DC = docker compose


app: # up dev processes
	$(DC) --env-file .env -f docker-compose.dev.yaml up -d	

stop: # stop all containers
	docker stop $$(docker ps -q)

delete: # delete all containers
	docker rm $$(docker ps -a -q)

bot_log:
	docker logs bot -f

test: # run tests
	$(DC) --env-file .env.test -f docker-compose.test.yaml up -d
	pytest . -s -v
	docker stop $$(docker ps -q)
	docker rm $$(docker ps -a -q)

restart:
	docker restart $$(docker ps -a -q)