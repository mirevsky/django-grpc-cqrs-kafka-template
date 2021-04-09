#!/bin/sh

echo " +----------------------------------------------------------+"
echo " |    Shell Script commands                                 |"
echo " +----------------------------------------------------------+"
echo " |   ./run_it.sh run query_controller                       |"
echo " |   ./run_it.sh run command_controller                     |"
echo " |   ./run_it.sh exec makemigrations                        |"
echo " |   ./run_it.sh exec migrate                               |"
echo " +----------------------------------------------------------+"

BASEDIR=$(dirname $0)

while [ "$1" != "" ]; do

  dockerize -wait tcp://mysql:3306 -timeout 1m -wait-retry-interval 10s

  case $1 in

  run | --run)
    case $2 in
      query_controller)
        python3 $BASEDIR/../domain_query_controller.py makemigrations
        python3 $BASEDIR/../domain_query_controller.py migrate
        python3 $BASEDIR/../domain_query_controller.py grpcrunserver 0.0.0.0:9000 --dev
        ;;
      command_controller)
        python3 $BASEDIR/../domain_command_controller.py
        ;;
    esac
    ;;

  exec | --exec)
    echo " EXECUTE: $2"
    python3 $BASEDIR/../domain_query_controller.py $2
    ;;

  esac
  shift
done