build:
	docker rmi monitoring-bot && docker build -t monitoring-bot .

run:
	HOST_UID="$(shell id -u)" HOST_GID="$(shell id -g)" \
	KNOWN_HOSTS_APP_PATH=/app/known_hosts \
	SSH_KEYS_APP_PATH=/app/ssh_keys \
	docker compose --env-file .env up -d

stop:
	HOST_UID="$(shell id -u)" HOST_GID="$(shell id -g)" \
	KNOWN_HOSTS_APP_PATH=/app/known_hosts \
	SSH_KEYS_APP_PATH=/app/ssh_keys \
	docker compose --env-file .env down

# run-only-docker:
# 	docker run -e SSH_KEYS_APP_PATH=/app/ssh_keys \
# 	-e KNOWN_HOSTS_APP_PATH=/app/known_hosts \
# 	-e UID="$(shell id -u)" -e GID="$(shell id -g)" \
# 	--name monitoring-container \
# 	-v ./ssh_keys:/app/ssh_keys:ro \
# 	-v ./servers-prod.yml:/app/servers-prod.yml:ro \
# 	-v ./.env:/app/.env:ro \
# 	-v ~/.ssh/known_hosts:/app/known_hosts monitoring-bot

# run-no-docker:
#	python bot.py