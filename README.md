# DASH Ingest Receiver

This project implements a simple server that receives live media from a broadcaster using the 
[DASH-IF Live Media Ingest Protocol](https://dashif-documents.azurewebsites.net/Ingest/master/DASH-IF-Ingest.html), stores them in a filesystem and then publishes them using [MPEG DASH](https://en.wikipedia.org/wiki/Dynamic_Adaptive_Streaming_over_HTTP).

For a complete demo you need a live broadcaster. You can use the open source [ABR Broadcaster](https://github.com/jkarthic-akamai/ABR-Broadcaster).

## Installation

Only Linux Debian/Ubuntu is supported. Please run the [install_debian.sh](install_debian.sh) script. 

TODO: A Dockerfile to make it run anywhere.

## Usage

Configure the broadcaster to push media to the URL <http://ip-address:9999/receiver>, e.g. for the ABR Broadcaster set the Ingest Base URL to this. Set Output Type to DASH and a suitable segment size, e.g. 5 seconds.

The receiver will store the received chunks and MDPs in a directory called `data`. MDPs are modified on the fly to ensure they are playable by the DASH player, e.g. `type` is set to `static` and `mediaPresentationDuration` is updated.

Apache errors are logged to `/var/log/apache2/dashreceiver-error_log`, please check it if you have problems.

The web interface can be accessed via <http://ip-address:9999/>. This implements a simple file browser to select which MDP to play in the [dash.js](https://github.com/Dash-Industry-Forum/dash.js) player.
