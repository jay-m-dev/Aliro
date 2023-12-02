#/bin/bash
# disable and remove bluetooth
# not needed in kiosk mode
#sudo systemctl disable hciuart.service
#sudo systemctl disable bluealsa.service
#sudo systemctl disable bluetooth.service
#sudo apt purge bluez -y
# remove unnecessary packages and clean up apt
# these are installed by the docker shell script
sudo apt remove docker-buildx-plugin -y
# these come pre-installed
sudo apt purge htop
sudo apt autoremove -y
sudo apt autoclean -y
sudo apt clean -y
# clean up logs
sudo journalctl --vacuum-time=7d
rm ~/get-docker.sh
# remove remaining logs
sudo rm -rf /var/log/*
sudo rm -rf /tmp/*
# remove scripts
rm /home/aliroed/*.sh
# clear bash history
history -c

