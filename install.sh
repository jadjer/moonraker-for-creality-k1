#!/bin/sh

set -e
clear

function set_paths() {
  # Colors #
  white=`echo -en "\033[m"`
  blue=`echo -en "\033[36m"`
  cyan=`echo -en "\033[1;36m"`
  yellow=`echo -en "\033[1;33m"`
  green=`echo -en "\033[01;32m"`
  darkred=`echo -en "\033[31m"`
  red=`echo -en "\033[01;31m"`

  # Paths #
  SERVICE_DIR="/etc/init.d"
  USERDATA_DIR="/usr/data"
  PRINTER_DATA_DIR="$USERDATA_DIR/printer_data"
  CONFIG_DIR="$PRINTER_DATA_DIR/config"

  for dir in "$SERVICE_DIR" "$USERDATA_DIR" "$PRINTER_DATA_DIR" "$CONFIG_DIR"; do
    if [ ! -d "$dir" ]; then
        echo "Error: $dir not found"
        exit 1
    fi
  done
}

function install() {
  ln -s ./config/moonraker.conf "$CONFIG_DIR"
  ln -s ./service/S56moonraker_service "$SERVICE_DIR"
}

function uninstall() {
  unlink "$CONFIG_DIR/moonraker.conf"
  unlink "$SERVICE_DIR/S56moonraker_service"
}

rm -rf /root/.cache
set_paths

if [ "$1" = "install" ]; then
  install
  return 0
fi

if [ "$1" = "uninstall" ]; then
  uninstall
  return 0
fi

echo "Usage: $0 [install|uninstall]"
