#!/bin/sh

host=$(echo $1 | cut -d ':' -f 1)
port=$(echo $1 | cut -d ':' -f 2)

shift 2

while ! mysqladmin ping -h "$host" -P "$port" -uuser -ppassword --silent; do
    >&2 echo "Database is unavailable - sleeping"
    sleep 2
done

>&2 echo "Database is up - executing command"
exec "$@"