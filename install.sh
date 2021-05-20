#!/bin/bash

# CONSTANTS
#HOME=$PWD
SYSD="/systemd"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

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
  template_path="${SCRIPT_DIR}${SYSD}/${template}.service"
  cp "${template_path}" "/etc/systemd/system/${template}.service"
  sed -i "s|PATH|${SCRIPT_DIR}|g" "/etc/systemd/system/${template}.service"

  if [ -d "${template_path}.d" ]; then
    cp -r "${template_path}.d" "/etc/systemd/system/"
  fi

  systemctl enable "${template}.service"
  systemctl start "${template}.service"
}

# chia-poolboys
delegate "Poolboys Tracker" "chia-poolboys"
