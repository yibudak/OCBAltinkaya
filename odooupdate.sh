#!/bin/bash
read -e -p "\n Enter odoo database name to update: " ODOODB
./openerp-server -d $ODOODB -u all --stop-after-init --config=/etc/odoo-server.conf
