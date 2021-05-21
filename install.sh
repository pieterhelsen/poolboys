#!/bin/bash

# CONSTANTS
#HOME=$PWD
LOG_DIR="/var/log/chia"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
CHIA_DIR="${HOME}/chia-blockchain/"

if [ ! -d "${LOG_DIR}" ]; then
  echo "Creating log directory: ${LOG_DIR}"
  mkdir LOG_DIR
  chown -R "${SUDO_USER} ${LOG_DIR}"
fi

if [ ! -d "${HOME}/chia-blockchain/" ]; then
  echo "Could not find chia-blockchain folder, please enter the path to the folder here."
  read -r CHIA_DIR
fi


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
  template_path="${SCRIPT_DIR}/systemd/${template}.service"
  cp "${template_path}" "/etc/systemd/system/${template}.service"
  sed -i "s|PATH|${SCRIPT_DIR}|g" "/etc/systemd/system/${template}.service"
  sed -i "s|CHIA|${CHIA_DIR}|g" "/etc/systemd/system/${template}.service"

  if [ -d "${template_path}.d" ]; then
    echo "Found override directory: ${template_path}.d"
    cp -r "${template_path}.d" "/etc/systemd/system/"
  fi

  systemctl daemon-reload
  systemctl enable "${template}.service"
  systemctl start "${template}.service"
}

# chia-poolboys
delegate "Poolboys Tracker" "chia-poolboys"
