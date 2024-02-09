#!/bin/bash

if [[ $(screen -ls | grep -c dapnet-ntfygateway) = 0 ]]; then
    screen -d -m -S dapnet-ntfygateway bash -c "cd $(dirname $0) && source ./venv/bin/activate && ./dapnet_ntfygateway.py"
else
    echo "screen session 'dapnet-ntfygateway' already running!"
fi
