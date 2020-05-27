#!/bin/bash
set -e
sudo apt update

# Dependencies for the receiver.
sudo apt install -y python python-pip python-dateutil
sudo apt install -y apache2 libapache2-mod-wsgi

# Dependencies for the web interface.
sudo apt install -y php
