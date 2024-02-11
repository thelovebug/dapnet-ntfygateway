#!/usr/bin/env bash

cd $(dirname "$0")

SCRIPTLOCATION=$(pwd)

croncmd="$SCRIPTLOCATION/monitor_helper.sh start"
cronjob="@reboot $croncmd"

case $1 in

mkcron)

    crontab -l | grep -F -i -v "$croncmd" | {
        cat
        echo "$cronjob"
    } | crontab -
    ;;

rmcron)

    crontab -l | grep -F -i -v "$croncmd" | crontab -
    ;;

start)

    if [[ $(screen -ls | grep -F -i -c dapnet-ntfygateway) = 0 ]]; then
        screen -d -m -S dapnet-ntfygateway bash -c "cd $(dirname "$0") && source ./venv/bin/activate && ./dapnet_ntfygateway.py"
    else
        echo "screen session 'dapnet-ntfygateway' already running!"
    fi
    ;;

stop)

    if [[ $(screen -ls | grep -F -i -c dapnet-ntfygateway) = 1 ]]; then
        screen -X -S dapnet-ntfygateway quit
    else
        echo "screen session 'dapnet-ntfygateway' wasn't running!"
    fi
    ;;

status)

    if [[ $(screen -ls | grep -F -i -c dapnet-ntfygateway) = 1 ]]; then
        echo "ntfygateway: running"
    else
        echo "ntfygateway: stopped"
    fi

    if [[ $(crontab -l | grep -F -i -c "$croncmd") = 1 ]]; then
        echo "crontab:     present"
    else
        echo "crontab:     not present"
    fi
    ;;

*)

    echo "usage: ./monitor_helper.sh COMMAND"
    echo ""
    echo "where COMMAND is one of the following:"
    echo ""
    echo "    start    - start the ntfygateway"
    echo "    stop     - stop the ntfygateway"
    echo "    status   - check the run/cron state of this process"
    echo "    mkcron   - add this process to cron to start on boot"
    echo "    rmcron   - remove this process from cron"
    echo ""
    ;;

esac
