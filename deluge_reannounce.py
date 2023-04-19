#!/usr/bin/env python2

# pip install deluge-client

import sys
import time
from deluge_client import DelugeRPCClient

# Get command line arguments for torrent ID, name, and path
torrent_id = sys.argv[1]
torrent_name = sys.argv[2]
torrent_path = sys.argv[3]

# Set up Deluge RPC client connection details
ip = "127.0.0.1"
port = 11111  # Change this to your Deluge daemon port
username = "str0ke"  # Change this to your Deluge username
password = "password"  # Change this to your Deluge password

# Set up loop parameters
max_iterations = 120
iteration_interval = 7

# Connect to the Deluge RPC client
client = DelugeRPCClient(ip, port, username, password)
client.connect()

# Loop for a maximum number of iterations
for i in range(max_iterations):
    
    # Sleep for the iteration interval
    time.sleep(iteration_interval)

    # Get torrent information
    torrent_info = client.call('core.get_torrent_status', torrent_id, [])

    # Check if the torrent is found
    if not torrent_info:
        print("Torrent not found or removed.")
        break

    # Get tracker status
    tracker_status = torrent_info.get(b'tracker_status', b'').decode('utf-8')

    # Force reannounce if tracker status indicates an issue
    if any(substr in tracker_status for substr in ['unregistered', 'Sent', 'End of file', 'Bad Gateway', 'Error']):
        client.call('core.force_reannounce', [torrent_id])
    else:
        # Get seed information
        seeds = torrent_info.get(b'num_seeds', 0)
        total_seeds = torrent_info.get(b'total_seeds', 0)
        print("Iteration {}: going through the iterations - Torrent ID: {}".format(i + 1, torrent_id))

        # If there are seeds, perform additional reannounces
        if seeds > 0 or total_seeds > 0:
            extra_iterations = 2
            extra_interval = 30

            for j in range(extra_iterations):
                time.sleep(extra_interval)
                client.call('core.force_reannounce', [torrent_id])

            print("Iteration {}: Found working torrent: {} {} {}".format(i + 1, torrent_name, torrent_path, torrent_id))
            break
        else:
            # Force reannounce if no seeds are found
            client.call('core.force_reannounce', [torrent_id])

# Disconnect from the Deluge RPC client
client.disconnect()
