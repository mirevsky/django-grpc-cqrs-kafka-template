#!/bin/sh

while [ "$1" != "" ]; do

  BASEDIR=$(dirname $0)

  case $1 in
  run | --run)

    case $2 in
    all)
      docker-compose up --build
      exit
      ;;

    integration)
      docker-compose up --build integration_tests
      exit
      ;;

    -s | --service | service)
      case $4 in
      -t | --test | test)
        docker-compose up -d $3
        docker-compose exec $3 bash -c "pytest"
        exit
        ;;

      -l | --lint | lint)
        docker-compose exec $3 bash -c "autopep8 /app --recursive --in-place --pep8-passes 2000 --verbose"
        docker-compose exec $3 bash -c "pylint /app"
        exit
        ;;

      *)
        docker-compose up --build $3
        exit
        ;;
      esac

      exit
      ;;

    -g | --grpc_tools | grpc_tools)
      source $BASEDIR/venv/bin/activate

      python3 -m grpc_tools.protoc -I ./app/shared/library/ --proto_path=$BASEDIR/app/shared/protoc/ --python_out=$BASEDIR/app/shared/library/ --grpc_python_out=$BASEDIR/app/shared/library/ $(find $BASEDIR/app/shared/protoc/ -name "*.proto")
      find $BASEDIR/app/shared/library/. -type d -exec touch {}/__init__.py \;

      sed -i -E 's/from component_a/from shared.library.component_a/g' $(find $BASEDIR/app/shared/library/ -name "*.py")

      exit
      ;;

    -l | --local | local)

      case $3 in
      -i | --install | install)

        sudo yum install python3-devel mysql-devel -y
        python3 -m venv $BASEDIR/venv
        pip3 install --upgrade pip
        source $BASEDIR/venv/bin/activate
        pip3 install -r $BASEDIR/app/requirements.txt
        exit
        ;;

      -u | --snapshot-update)

        cd $BASEDIR/app
        export PYTHONPATH=$PYTHONPATH:$PWD/component_a
        pip3 install --upgrade pip
        source $PWD/../venv/bin/activate
        pip3 install -r $PWD/requirements.txt
        pytest $PWD/component_a --snapshot-update


        cd $BASEDIR/integration_tests
        export PYTHONPATH=$PYTHONPATH:$PWD/integration_tests
        pip3 install --upgrade pip
        source $PWD/../venv/bin/activate
        pip3 install -r $PWD/requirements.txt
        pytest $PWD/integration_tests --snapshot-update

        exit
        ;;

      esac

      python3 -m grpc_tools.protoc -I ./app/shared/library/ --proto_path=$BASEDIR/app/shared/protoc/ --python_out=$BASEDIR/app/shared/library/ --grpc_python_out=$BASEDIR/app/shared/library/ $(find $BASEDIR/app/shared/protoc/ -name "*.proto")
      find $BASEDIR/app/shared/library/. -type d -exec touch {}/__init__.py \;

      sed -i -E 's/from component_a/from shared.library.component_a/g' $(find $BASEDIR/app/shared/library/ -name "*.py")

      exit
      ;;
    esac
    exit
    ;;

  restart | --restart)
    docker-compose restart $2
    exit
    ;;

  exec | --exec)
    docker-compose exec $2 /bin/bash
    exit
    ;;

  kill | --kill)

    case $2 in
    all)
      docker kill $(docker ps -q)
      exit
      ;;
    esac

    exit
    ;;

  delete | --delete)

    case $2 in
    all)
      docker kill $(docker ps -q)
      docker system prune
      docker system prune --volumes
      docker rmi $(docker images -a -q)
      exit
      ;;
    esac

    exit
    ;;

  -h | --help | help)

    echo " +----------------------------------------------------------------------------------------------+"
    echo " |                        ::.......................................:--                          |"
    echo " |                      :-:.....................................:--=+=                          |"
    echo " |                    .----:.................................::----=++=.                        |"
    echo " |                   .------:..............................:------=+++++:                       |"
    echo " |                  .--------:..........................::--------=++++++:                      |"
    echo " |                 :----------:.......................:-----------++++++++-                     |"
    echo " |                :-----------:.....................:------------=+++++++++-                    |"
    echo " |               :-------------:.................::--------------=++++++++++=                   |"
    echo " |              ----------------:..............:----------------=++++++++++++=.                 |"
    echo " |            .------------------:...........:------------------=+++++++++++++=.                |"
    echo " |           .--------------------:.......::--------------------++++++++++++++++:               |"
    echo " |          :---------------------:.....:----------------------=+++++++++++++++++:              |"
    echo " |         :-----------------------:..:------------------------=++++++++++++++++++-             |"
    echo " |        :---------------------------------------------------=++++++++++++++++++++-            |"
    echo " |       :--------------------------=+==----------------------=+++++++++++++++++++++=           |"
    echo " |      ---------------------------=++++==--------------------+++++++++++++++++++++++=.         |"
    echo " |    .----------------------------=++++++==-----------------=++++++++++++++++++++++++=.        |"
    echo " |   .----------------------------=++++++++++=---------------=++++++++++++++++++++++++++:       |"
    echo " |  .-----------------------------=++++++++++++==-----------=++++++++++++++++++++++++++++.      |"
    echo " |   .---------------------------=+++++++++++++++==---------=+++++++++++++++++++++++++++:       |"
    echo " |    .--------------------------=+++++++++++++++++==-------+++++++++++++++++++++++++++.        |"
    echo " |      ------------------------=+++++++++++++++++++++=----=++++++++++++++++++++++++++          |"
    echo " |       -----------------------=+++++++++++++++++++++++==-=++++++++++++++++++++++++=           |"
    echo " |        :---------------------++++++++++++++++++++++++++=++++++++++++++++++++++++-            |"
    echo " |         :-------------------=+++++++++++++++++++++++=====++++++++++++++++++++++-             |"
    echo " |          :------------------++++++++++++++++++++++=======+++++++++++++++++++++:              |"
    echo " |           .----------------=+++++++++++++++++++===========+++++++++++++++++++.               |"
    echo " |            .---------------++++++++++++++++++==============+++++++++++++++++.                |"
    echo " |              -------------=++++++++++++++++================+++++++++++++++=                  |"
    echo " |               ------------++++++++++++++====================+++++++++++++=                   |"
    echo " |                :---------=++++++++++++=======================+++++++++++-                    |"
    echo " |                 :--------=+++++++++==========================++++++++++:                     |"
    echo " |                  .------=++++++++=============================++++++++:                      |"
    echo " |                   .-----=+++++=================================++++++.                       |"
    echo " |                     ---=++++====================================++++.                        |"
    echo " |                      --=+=======================================++=                          |"
    echo " |                       :=------------------------------------------                           |"
    echo " |   Emerald Plus Microservice Command Tool                                                     |"
    echo " |   www.emerald.plus                                                                           |"
    echo " +----------------------------------------------------------------------------------------------+"
    echo " |   ./app.sh run all                                                                           |"
    echo " |   ./app.sh run integration                                                                   |"
    echo " |   ./app.sh run service component_a_command                                                   |"
    echo " |   ./app.sh run service component_a_command test                                              |"
    echo " |   ./app.sh run service component_a_command lint                                              |"
    echo " |                                                                                              |"
    echo " |   ./app.sh run local install                                                                 |"
    echo " |   ./app.sh run local --snapshot-update                                                       |"
    echo " |   ./app.sh run grpc_tools                                                                    |"
    echo " |                                                                                              |"
    echo " |   ./app.sh exec component_a_command                                                          |"
    echo " |   ./app.sh restart component_a_command                                                       |"
    echo " |                                                                                              |"
    echo " |   ./app.sh kill all                                                                          |"
    echo " |                                                                                              |"
    echo " |   ./app.sh delete all                                                                        |"
    echo " +----------------------------------------------------------------------------------------------+"
    exit
    ;;
  esac
  shift
done
