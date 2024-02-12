#!/usr/bin/env bash

# Get script path location
TEMP=$(dirname "$0")
cd "$TEMP" || return
SCRIPTLOCATION="$(pwd)"

# Get current script name (i.e. this script)
TEMP=$(basename "$0")
SCRIPTFILENAME="$TEMP"

SCRIPTFULLNAME="$SCRIPTLOCATION/$SCRIPTFILENAME"

croncmd="$SCRIPTFULLNAME start"
cronjob="@reboot $croncmd"

case $1 in

enable)

    crontab -l | grep -F -i -v "$croncmd" | {
        cat
        echo "$cronjob"
    } | crontab -
    ;;

disable)

    crontab -l | grep -F -i -v "$croncmd" | crontab -
    ;;

start)

    if [[ $(screen -ls | grep -F -i -c dapnet-ntfygateway) = 0 ]]; then
        screen -d -m -S dapnet-ntfygateway bash -c "cd \"$SCRIPTLOCATION\" && source ./venv/bin/activate && ./dapnet_ntfygateway.py"
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
        echo "script is:        RUNNING"
    else
        echo "script is:        STOPPED"
    fi

    if [[ $(crontab -l | grep -F -i -c "$croncmd") = 1 ]]; then
        echo "start on boot is: ENABLED"
    else
        echo "start on boot is: DISABLED"
    fi
    ;;

update)

    echo "Starting update process..."
    echo ""
    # Create a new temporary file, which will form the second part of our update process
    TEMPFILE=$(mktemp)

    # Start the update script with a shebang
    echo "#!/usr/bin/env bash" >>"$TEMPFILE"

    # Change to the script execution directory, and perform a git pull (the actual update)
    echo "echo \"\"" >>"$TEMPFILE"
    echo "cd \"$SCRIPTLOCATION\"" >>"$TEMPFILE"
    echo "echo \"* Pulling updates from git repo...\"" >>"$TEMPFILE"
    echo "echo \"\"" >>"$TEMPFILE"
    echo "git pull" >>"$TEMPFILE"
    echo "echo \"\"" >>"$TEMPFILE"

    # If monitor script is currently running, stop it, and make sure it's restarted after update
    if [[ $(screen -ls | grep -F -i -c dapnet-ntfygateway) = 1 ]]; then
        echo "* Stopping monitor script..."
        "$SCRIPTFULLNAME" stop
        echo "echo \"* Starting monitor script...\"" >>"$TEMPFILE"
        echo "\"$SCRIPTFULLNAME\" start" >>"$TEMPFILE"
    fi

    # If start at boot is currently enabled, disable it, and make sure it is reenabled after update
    if [[ $(crontab -l | grep -F -i -c "$croncmd") = 1 ]]; then
        echo "* Disabling start at boot..."
        "$SCRIPTFULLNAME" disable
        echo "echo \"* Enabling start at boot...\"" >>"$TEMPFILE"
        echo "\"$SCRIPTFULLNAME\" enable" >>"$TEMPFILE"
    fi

    echo "echo \"\" " >>"$TEMPFILE"
    echo "echo \"All updates complete.\" " >>"$TEMPFILE"

    # Make update script executeable, execute it, delete it
    chmod +x "$TEMPFILE"
    exec "$TEMPFILE"
    rm "$TEMPFILE"

    ;;

*)

    echo "usage: ./monitor_helper.sh COMMAND"
    echo ""
    echo "where COMMAND is one of the following:"
    echo ""
    echo "    start    - start the ntfygateway"
    echo "    stop     - stop the ntfygateway"
    echo "    status   - check the run/cron state of this process"
    echo "    enable   - allow this process to start on boot"
    echo "    disable  - remove this process from starting on boot"
    echo "    update   - update the code and restart the script (if running)"
    echo ""
    ;;

esac
