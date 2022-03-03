dev:
	docker-compose -f docker-compose.yml -p movieguessr_dev up

prod:
	docker build -t idylank/movieguessr:web app -f app/Dockerfile.prod
	docker build -t idylank/movieguessr:nginx nginx
	docker-compose -f docker-compose.prod.yml -p movieguessr_prod up --detach

test:
	docker-compose -f docker-compose.yml -p movieguessr_dev up --detach

stop:
	docker ps -a -q | ( while read ID; do docker stop $$ID; done )

kill:
	docker ps -a -q | ( while read ID; do docker kill $$ID; done )

# !! Stop & Remove all existing containers: USE WITH CARE !!
rm:
	docker ps -a -q | ( while read ID; do docker stop $$ID; done )
	docker ps -a -q | ( while read ID; do docker rm $$ID; done )
	
rm-images:
	docker ps -a -q | ( while read ID; do docker stop $$ID; done )
	docker images -a -q | ( while read ID; do docker rmi -f $$ID; done )

build-hub:
	docker build -t idylank/movieguessr:web app -f app/Dockerfile.prod
	docker build -t idylank/movieguessr:nginx nginx
	docker push idylank/movieguessr:web
	docker push idylank/movieguessr:nginx