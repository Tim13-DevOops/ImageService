#!/bin/sh
# wait-for-postgres.sh
  


if [ "$COMMAND" = "run_server" ]
then
  # python setup.py install
  # start_image_server
  cd app
  python app.py
fi

exec "$@"

