# `dapnet-ntfygateway`

Picks up DAPNET calls from an MMDVM node, and forwards it to a [ntfy.sh](https://ntfy.sh/) topic.

## What is it?

Ultimately, this is designed to be installed on an MMDVM node running [Pi-star](http://www.pistar.uk/) or [WPSD](https://wpsd.radio/).

It sits and reads the logfile located at:

`/var/log/pi-star/DAPNETGateway-yyyy-mm-dd.log`

... extracts information relating to pages received that are intended for you (or a fellow Amateur operator), and then forwards that page through to a [ntfy.sh](https://ntfy.sh/) topic so that they can be received on the official ntfy.sh app or picked up by another script that is subscribed to that topic.

## Why?

Because:

* you may not always have your pager with you
* you may not always be in range of a DAPNET transmitter
* you may not have a pager at all, but you still want to experience the fun of the DAPNET system
* you may be using the DAPNET Telegram bot, which only works on a handful of transmitter groups (and specifically *not* `uk-all`)
* why not?

## Installation

Visit [INSTALL.md](INSTALL.md) for full installation instructions.

## To do

* ✅ ~~Document the installation process~~ Done, kinda.
* Document the `config.json` file
* Error handling - like, any!
* Expand the informational message scope to include DAPNET network connection status
* Profit!! *(only joking!)*

## Contributors

A huge thank you from me to the following individuals who have contributed to this project:

* [thelovebug](https://github.com/thelovebug) - that's me!  Thanks, me!  You're welcome, me!
* [guinuxbr](https://github.com/guinuxbr) - code contributions and teaching me how to do stuff the right way
* [CtrlAltDel-Irl](https://github.com/CtrlAltDel-Irl) - testing, support, and inspiration
* [vk3xem](https://github.com/vk3xem) - the first production user of this project, and also helped me to hone the installation process

## This project was made for the Amateur Radio community with ❤ by Dave [M7TLB](https://qrz.com/db/M7TLB)
