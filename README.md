# MovieGuessr

## Dependencies
- Make sure that Docker and Docker-compose are installed
- Make sure that the Docker daemon is running. On most Linux distributions this can be done by running `systemctl start docker`  

## Development
- Build and/or run using: `make dev` running on port 8000. The application is available at localhost:8000
- The .env.dev is used for environment settings.
- Database migrations and collectstatic are done on every boot.
- To run database migrations manually: `docker exec web_dev python3 manage.py migrate`
- To set the static folder: `docker exec web_dev python3 manage.py collectstatic --noinput`


## Production
- To run database migrations manually: `...`
- To set the static folder: `...`

