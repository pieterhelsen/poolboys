#!/bin/bash

# CONSTANTS
HOME=$PWD
SYSD="/systemd"

# FUNCTIONS
delegate(){
  name=$1
  service=$2

  echo "Do you want to install $name? (Y)es/(N)o"
  read -r input

  if [ "$input" = "yes" ] || [ "$input" = "y" ] || [ "$input" = "Yes" ] || [ "$input" = "Y" ]
  then
    create "$service"
    echo -e "\nSuccessfully installed ${name} service!"
  elif [ "$input" = "quit" ] || [ "$input" = "q" ]
  then
    echo -e "\nClosing setup script"
    exit 0
  else echo -e "\n$name not installed."
  fi

  echo -e "---\n"
}

create(){
  template=$1
  cp "${HOME}${SYSD}/${template}.service" "/etc/systemd/system/${template}.service"
  systemctl enable "${template}.service"
  systemctl start "${template}.service"
}

# chia-poolboys
delegate "Poolboys Tracker" "chia-poolboys"
