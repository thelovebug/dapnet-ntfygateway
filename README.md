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

## Installation

*You should only ever need to do this once - unless you totally b0rk it!*

You'll need SSH access to your MMDVM node. Start off by making sure you have the correct software installed to run this script:

If you use Ubuntu or another Debian based Linux distribution:

```shell
sudo apt update
```

```shell
sudo apt install git python3 python3-venv screen
```

It's likely you'll already have `python3` installed, but it doesn't hurt to check.  It's also kinda necessary.

Now download and set up the environment for the tool:

Create the folder for the script and download it:

```shell
mkdir -p ~/git
```

```shell
cd ~/git
```

```shell
git clone https://github.com/thelovebug/dapnet-ntfygateway
```

```shell
cd dapnet-ntfygateway
```

Set up the environment to run it and download dependencies:

```shell
python3 -m venv venv
```

```shell
source ./venv/bin/activate
```

```shell
pip install -r requirements.txt
```

There, all installed.  Next thing is to prep your config file.

Copy the sample config into the live location:

```shell
cp config.json.example config.json
```

Now edit your `config.json` file in your favourite text editor.  The bits to change are self-explanatory, but here's a guide:

```json
"profiles": {
    "anyname": {                            # change anyname to something that helps you identify this profile - your DMR ID perhaps?
        "ric": "your-ric",                  # change your-ric to the RIC provided by DAPNET, it's usually a variation on your DMR ID
        "call": "your-callsign",            # change your-callsign to - guess what? - your callsign, case isn't important
        "endpoint": "your-ntfy-endpoint",   # change your-ntfy-endpoint, it'll start with https://ntfy.sh/ - check that website for info
        "enabled": true,                    # everything else can stay as is for now
        "alertoncall": true,
        "messagetypes": [
            "M",
            "E",
            "I",
            "D"
        ]
    }
}
```

You're ready to go!

## Running the script

To kick the script off, enter the following command:

``` shell
./monitor_helper.sh start
```

This will start the process in a detached `screen` session.

If you want to make sure that this script starts on boot, then use the following command:

```shell
./monitor_helper.sh enable
```

If you want to know if the script is running, or if the script is set to start on boot, use the following command:

```shell
./monitor_helper.sh status
```

Good luck, and reach out to me (via [QRZ](https://qrz.com/db/M7TLB)) if you have any issues.

## To do

* ~~Document the installation process~~ Done, kinda.
* Document the `config.json` file
* Error handling - like, any!
* Expand the informational message scope to include DAPNET network connection status
* Profit!!

_(only joking on that last bit, this project was made with ❤ by Dave [M7TLB](https://qrz.com/db/M7TLB) in South Yorkshire, UK)_
