#!/bin/bash

if [[ $(screen -ls | grep -c dapnet-ntfygateway) = 1 ]]; then
    screen -X -S dapnet-ntfygateway quit
else
    echo "screen session 'dapnet-ntfygateway' wasn't running!"
fi
