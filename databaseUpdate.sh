#!/bin/bash

if [ "$(id -u)" = "0" ]; then
   echo "This script must not be run as root" 1>&2
   exit 1
fi

read -e -p "Enter odoo database name to update: " ODOODB

while true; do
    read -p "Would you like to update odoo database all  modules odoo server will stop  (y/n)?" yn
    case $yn in
        [Yy]* ) 
        sudo /etc/init.d/odoo-server stop
        sudo service odoo stop
        echo -e "Updating Database"
        ./openerp-server -d $ODOODB -u all --stop-after-init --config=/etc/odoo-server.conf --workers=0 --max-cron-threads=0
        sudo /etc/init.d/odoo-server start
        sudo service odoo start
        break;;
        [Nn]* ) break;;
        * ) echo "Please answer yes or no.";;
    esac
done

