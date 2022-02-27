dev:
	docker-compose -f docker-compose.yml -p movieguessr_dev up

prod:
	docker-compose -f docker-compose.prod.yml -p movieguessr_prod up

test:
	docker-compose -f docker-compose.yml -p movieguessr_dev up --detach

# !! Stop & Remove all existing containers: USE WITH CARE !!
rm:
	docker ps -a -q | ( while read ID; do docker stop $$ID; done )
	docker ps -a -q | ( while read ID; do docker rm $$ID; done )
	
rm-images:
	docker ps -a -q | ( while read ID; do docker stop $$ID; done )
	docker images -a -q | ( while read ID; do docker rmi -f $$ID; done )
