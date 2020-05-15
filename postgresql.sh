#!/bin/sh

echo "Starting Postgresql.."
docker run --rm --name coinpaprika -e POSTGRES_PASSWORD=docker -d -p 5432:5432 -v $(pwd)/postgres:/var/lib/postgresql/data postgres

psql -h localhost -U postgres -d postgres    