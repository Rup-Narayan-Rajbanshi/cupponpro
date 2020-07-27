#!/bin/sh

set -e
set -u



PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# Delete old version
cd "$PROJECT_ROOT"

echo ""
echo "## IMPORT GIT FILES TO DEVELOPMENT ENVIRONMENT (WITH DOCKER)"
echo ""

echo "Stopping existing containers"
{
	docker-compose --no-ansi kill || die "ERROR: unable to stop containers"
}

echo "Removing existing containers"
{
	docker-compose --no-ansi rm -f || die "ERROR: unable to remove containers"
}

# Rebuild container
echo "Building container from sources"
{
 	docker-compose --no-ansi build || die "ERROR: unable to build containers"
}

echo "Running new container"
{
	docker-compose --no-ansi up || die "ERROR: unable to start containers"
}

# echo "Waiting for database to be ready"
# {
# 	while ! nc -vz localhost 3306; do
# 		echo "Trying to access the db"
# 		sleep 1
# 	done
# }

echo "Importing SQL file into database"
sleep 10
{
	./docker/db-import-from-file  || die "ERROR: unable to import database"
}

echo "Success!"
