COMPOSE_DEV := docker compose -f docker-compose.yml

up:
	$(COMPOSE_DEV) up -d --build
stop:
	$(COMPOSE_DEV) stop
down:
	$(COMPOSE_DEV) down -v
restart:
	$(COMPOSE_DEV) up -d --build bot
logs:
	$(COMPOSE_DEV) logs -f --tail bot
clean:
	$(COMPOSE_DEV) exec redis redis-cli FLUSHALL

freeze:
	rm requirements.txt && pip freeze >> requirements.txt && git add requirements.txt
