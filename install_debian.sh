#!/bin/bash
set -e

git clone https://github.com/jqueryfiletree/jqueryfiletree.git

install/others_debian.sh
install/apache_config.sh /etc/apache2/apache2.conf /etc/apache2/sites-enabled/010-dashreceiver.conf

mkdir -p data
sudo chown www-data:www-data data
sudo service apache2 reload
