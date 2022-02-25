dev:
	docker-compose -f docker-compose.yml -p movieguessr_dev up

prod:
	docker-compose -f docker-compose.prod.yml -p movieguessr_prod up