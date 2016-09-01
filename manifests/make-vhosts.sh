#!/usr/bin/env bash

## Only thing you probably really care about is right here
DOMAINS=(
    "wp.local"
)

## Loop through all sites
for ((i=0; i < ${#DOMAINS[@]}; i++)); do

    ## Current Domain
    DOMAIN=${DOMAINS[$i]}

    echo "Creating directory for $DOMAIN..."
    mkdir -p /var/www/$DOMAIN/public

    echo "Creating vhost config for $DOMAIN..."
    sudo cp /etc/apache2/sites-available/temp.local.conf /etc/apache2/sites-available/$DOMAIN.conf

    echo "Creating symbolic link"
    sudo ln -s /etc/apache2/sites-available/$DOMAIN.conf /etc/apache2/sites-enabled/$DOMAIN.conf

    echo "Updating vhost config for $DOMAIN..."
    sudo sed -i s,temp.local,$DOMAIN,g /etc/apache2/sites-available/$DOMAIN.conf
    sudo sed -i s,/var/www/temp,/var/www/$DOMAIN/public,g /etc/apache2/sites-available/$DOMAIN.conf

    echo "Enabling $DOMAIN. Will probably tell you to restart Apache..."
    sudo a2ensite $DOMAIN.conf

    # echo "So let's restart apache..."
    # sudo service apache2 restart

done
