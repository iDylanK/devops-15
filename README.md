# MovieGuessr

## Development
- Build and/or run using: `make dev`
- The .env.dev is used for environment settings.
- Database migrations and collectstatic are done on every boot.
- To run database migrations manually: `docker exec web_dev python3 manage.py migrate`
- To set the static folder: `docker exec web_dev python3 manage.py collectstatic --noinput`


## Production
- To run database migrations manually: `...`
- To set the static folder: `...`
