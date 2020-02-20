#!/usr/bin/env bash

# Color codes & helper functions
red=$(tput setaf 1)
green=$(tput setaf 2)
yellow=$(tput setaf 3)
blue=$(tput setaf 4)
magenta=$(tput setaf 5)
cyan=$(tput setaf 6)
white=$(tput setaf 7)
reset=$(tput sgr0)

debug=0

debugMode () {
if [ "$debug" -eq 1 ]; then
  echo "$1"
fi
}

# Prechecks

if [ "$#" -lt 3 ]; then
  debugMode "${red}More arguments required.${reset}"
  debugMode -e "$0 username \"Person's Name <email@example.com\" \"ssh-key\" [--admin]"
  exit 1
fi

if [[ $EUID -ne 0 ]]; then
  debugMode "This script must be run as root"
  exit 1
fi

debugMode "${yellow}Username:${reset} $1"
debugMode "${yellow}Name and Email:${reset} $2"
debugMode "${yellow}SSH PublicKey file:${reset} $3"

if [ ! -d "/home/$1/" ]; then
  useradd "$1" --comment "$2"
  echo "${green}Created user <$1>.${reset}"
else
  echo "${yellow}User already exist.${reset}"
fi

if [ ! -d "/home/$1/.ssh" ]; then
  mkdir -p "/home/$1/.ssh"
  debugMode "${green}Creating user's SSH directory.${reset}"
else
  debugMode "${yellow}User's ssh folder already exist.${reset}"
fi

debugMode "${yellow}Updating the authorized_keys file${reset}"
cat "$3" > "/home/$1/.ssh/authorized_keys"

debugMode "${yellow}Setting permissions.${reset}"
chmod 700 "/home/$1/.ssh"
chmod 600 "/home/$1/.ssh/authorized_keys"
chown -R "$1":"$1" "/home/$1/.ssh"

if [ "$4" = "--admin" ]; then
  echo "${yellow}Setting Admin privileges.${reset}"
  usermod -aG wheel "$1"
  sed 's/# %wheel/%wheel/g' -i /etc/sudoers  
fi

echo "${green}Created user (${yellow}$1${green}) for $2.${reset}"
