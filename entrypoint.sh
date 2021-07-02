#!/bin/sh
# wait-for-postgres.sh
  


if [ "$COMMAND" = "run_server" ]
then
  python setup.py install
  start_server
fi

exec "$@"

