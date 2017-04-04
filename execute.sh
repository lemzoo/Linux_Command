#!/bin/bash
#
# TEST          Start/Stop our TEST example script.
#
# chkconfig: 2345 90 60
# description: This is a simple service script that was made to demonstrate \
# how to write SysVinit scripts to 'daemonize' programs.
#

# Directory which contains the project
work_home=$HOME/works/siaef_projects

case "$1" in
    start_backend)
        echo "Launching the backend"

        # 1. Set environment variable
        cd $work_home/
        echo "Set the environment variable"
        source env_variable.export

        # 2. Set the venv
        echo "Setting virtual environment"
        # deactivate
        cd $work_home/sief-back/
        source venv/bin/activate

        # 3. Launch the server
        echo "Start backend server"
        kill -9 $(lsof -i:5000 -t) 2> /dev/null
        ./manage.py runserver -dr
        echo "Positional parameter 1 contains something"
	   ;;

    start_frontend)
        cd $work_home/sief-front/
        echo "Launching the frontend"
        kill -9 $(lsof -i:9000 -t) 2> /dev/null
        grunt serve
        ;;

    start_solr)
        # 1. Launch SOLR
        cd $work_home/dependencies/solr-5.1.0/
        echo "Launching SOLR"
        kill -9 $(lsof -i:8983 -t) 2> /dev/null
        ./bin/solr start
        ;;

    update_datamodel)
        # Goto mongo dumps
        cd $work_home/mongo_dumps/qualif

        # Use mongorestore
        mongorestore sief/ -d sief --drop
        mongorestore sief-broker/ -d sief-broker --drop

        # source the venv
        cd $work_home/sief-back/
        source venv/bin/activate

        # Upgrade datamodel
        ./manage.py datamodel upgrade -y

        # Clear solr
        ./manage.py solr clear -y

        # Build solr
        ./manage.py solr build -y
        ;;

    start_rabbit)
        echo "Starting rabbitmq server"
        sudo rabbitmqctl start_app
        ;;

    stop_rabbit)
        # Stop rabbitmq server
        echo "Stopping rabbitmq server"
        sudo rabbitmqctl stop_app
        ;;

    reset_rabbit)
        echo "Reseting rabbit"
        sudo rabbitmqctl stop_app
        sudo rabbitmqctl reset
        sudo rabbitmqctl start_app
        # add user 'developer' with password 'P@ssw0rd'
        sudo rabbitmqctl add_user developer P@ssw0rd
        # add virtual host 'siaef'
        sudo rabbitmqctl add_vhost siaef
        # add user tag 'developer' for user 'guest'
        sudo rabbitmqctl set_user_tags developer administrator
        # set permission for user 'jimmy' on virtual host 'jimmy_vhost'
        sudo rabbitmqctl set_permissions -p siaef developer ".*" ".*" ".*"
        sudo rabbitmqctl set_permissions -p siaef guest ".*" ".*" ".*"
        ;;

    venv)
        # Directory which contains the project
        work_home=$HOME/works/siaef_projects/

        # Start python environment
        cd $work_home/sief-back/
        deactivate
        source venv/bin/activate
        echo "Starting virtual environment for python 3.4"
        ;;

    variable_environment)
        # 1. Set environment variable
        cd $work_home/
        echo "Setting the environment variable ..."
        source env_variable.export
        ;;
    *)
        echo "usage : $0 <start_backend|start_frontend|start_solr|update_datamodel|
                          start_rabbit|stop_rabbit|reset_rabbit|venv|variable_environment|>" >&2
	exit 1
esac
exit 0
