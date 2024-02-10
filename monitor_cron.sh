#!/usr/bin/env bash

cd $(dirname "$0")

SCRIPTLOCATION=$(pwd)

croncmd="$SCRIPTLOCATION/monitor_start.sh"
cronjob="@reboot $croncmd"


case $1 in
add)
    crontab -l | fgrep -i -v "$croncmd" | {
        cat
        echo "$cronjob"
    } | crontab -
    ;;
remove)
    crontab -l | fgrep -i -v "$croncmd" | crontab -
    ;;
esac
