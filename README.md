# dapnet-ntfygateway

Full documentation to follow!

## What is it?

Ultimately, this is designed to be installed on an MMDVM node running [Pi-star](http://www.pistar.uk/) or [WPSD](https://wpsd.radio/).

It sits and reads the logfile located at:

`/var/log/pi-star/DAPNETGateway-yyyy-mm-dd.log`

... extracts information relating to pages received that are intended for you (or a fellow Amateur operator), and then forwards that page through to a [ntfy.sh](https://ntfy.sh/) topic so that they can be received on the official ntfy.sh app or picked up by another script that is subscribed to that topic.

## Why?

Because:

* you may not always have your pager with you
* you may not always be in range of a DAPNET transmitter
* you may be using the DAPNET Telegram bot, which only works on a handful of transmitter groups (and specifically _not_ `uk-all`)
* why not?

## To do

* Document the installation process
* Document the `config.json` file
* Profit!!

_(only joking on that last bit, this project was made with ❤ by Dave [M7TLB](https://qrz.com/db/M7TLB) in South Yorkshire, UK)
