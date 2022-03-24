dev:
	docker-compose -f docker-compose.yml -p movieguessr_dev up

test:
	docker-compose -f docker-compose.yml -p movieguessr_dev up --detach

prod:
	docker build -t idylank/movieguessr:web app --target prod
	docker build -t idylank/movieguessr:nginx nginx
	docker push idylank/movieguessr:web
	docker push idylank/movieguessr:nginx

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

#manual commands
compose-manage-py:
	docker-compose run --rm $(options) web_dev python3 manage.py $(cmd)