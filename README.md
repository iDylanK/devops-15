# MovieGuessr

## Development
- Build and/or run using: `make dev`
- The .env.dev is used for environment settings.
- Database migrations are done on every boot.
- To run database migrations manually: `docker exec web_dev python3 manage.py migrate`
- To set the static folder: `docker exec web_dev python3 manage.py collectstatic --noinput`


## Production
- Build and/or run using: `make prod`
- The .env.prod is used for environment settings (has to be created).
- To run database migrations manually: `docker exec web_prod python3 manage.py migrate`
- To set the static folder: `docker exec web_prod python3 manage.py collectstatic --noinput`
