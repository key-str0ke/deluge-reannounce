
# Deluge Torrent Reannounce Script

This Python script helps automate reannouncing torrents in Deluge to improve the chances of finding seeds. It uses the `deluge-client` package to communicate with the Deluge daemon.

<br>

## Installation

1. Install the required package:

```
pip install deluge-client
```
<br>

## Usage

Use the following command to run the script:

```
python deluge_reannounce.py <torrent_id> <torrent_name> <torrent_path>
```

Replace `<torrent_id>`, `<torrent_name>`, and `<torrent_path>` with the appropriate values for your torrent.

or

Use the following shell script for logging:

```
#!/bin/bash

torrentid="$1"
torrentname="$2"
torrentpath="$3"

python deluge_reannounce.py "$torrentid" "$torrentname" "$torrentpath" >> ~/logs/deluge_reannounce.log
```

## Configuration

Before running the script, make sure to update the following variables in the script with your Deluge connection details:

```
ip = "127.0.0.1"
port = 19045  # Change this to your Deluge daemon port
username = "str0ke"  # Change this to your Deluge username
password = "password"  # Change this to your Deluge password
```

<br>

## How It Works

The script connects to the Deluge RPC client and goes through a loop with a maximum number of iterations (configurable). It sleeps for a specified interval between iterations and then checks the torrent information, including the tracker status and seed information. If the script finds seeds or specific tracker issues, it will force a reannounce to improve the chances of downloading the torrent.
