# MovieGuessr

## Dependencies
- Make sure that Docker and Docker-compose are installed
- Make sure that the Docker daemon is running. On most Linux distributions this can be done by running `systemctl start docker`  

## Development
- Build and/or run using: `make dev` running on port 8000. The application is available at localhost:8000
- The .env.dev is used for environment settings.
- Database migrations and collectstatic are done on every boot.
- To run database migrations manually: `docker exec web_dev python3 manage.py migrate`
- To set the static folder manually : `docker exec web_dev python3 manage.py collectstatic --noinput`

## Linting
- Before committing, check django linting using: `make lint`

## Testing
To perform an execute of the Django tests, outside of CI/CD, please do the following:
- Ensure the server is running (see development section above).
- Execute the tests with `make test`

## Production
- Runs on AWS.
- Migrations and collecting static files are done automatically.

