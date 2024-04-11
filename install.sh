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

function top_line() {
  echo -e "${white}"
  echo -e " ┌──────────────────────────────────────────────────────────────┐"
}

function hr() {
  echo -e " │                                                              │"
}

function inner_line() {
  echo -e " ├──────────────────────────────────────────────────────────────┤"
}

function bottom_line() {
  echo -e " └──────────────────────────────────────────────────────────────┘"
  echo -e "${white}"
}

function main_menu_option() {
  local menu_number=$1
  local menu_text1=$2
  local menu_text2=$3
  local max_length=56
  local total_text_length=$(( ${#menu_text1} + ${#menu_text2} ))
  local padding=$((max_length - total_text_length))
  printf " │  ${yellow}${menu_number}${white}) ${green}${menu_text1} ${white}${menu_text2}%-${padding}s${white}│\n" ''
}

function bottom_menu_option() {
  local menu_number=$1
  local menu_text=$2
  local color=$3
  local max_length=57
  local padding=$((max_length - ${#menu_text}))
  printf " │  $color${menu_number}${white}) ${white}${menu_text}%-${padding}s${white}│\n" ''
}

function menu_ui() {
  top_line
  hr
  main_menu_option '1' '[Install]' 'Menu'
  main_menu_option '2' '[Remove]' 'Menu'
  hr
  inner_line
  hr
  bottom_menu_option 'q' 'Exit' "${darkred}"
  hr
  bottom_line
}

function install() {
  ln -s ./config/moonraker.conf "$CONFIG_DIR"
  ln -s ./service/S56moonraker_service "$SERVICE_DIR"
}

function uninstall() {
  unlink "$CONFIG_DIR/moonraker.conf"
  unlink "$SERVICE_DIR/S56moonraker_service"
}

function menu() {
  clear
  menu_ui
  local menu_opt
  while true; do
    read -p "${white} Type your choice and validate with Enter: ${yellow}" menu_opt
    case "${menu_opt}" in
      1) clear
         install
         break;;
      2) clear
         uninstall
         break;;
      Q|q)
         clear; exit 0;;
      *)
         error_msg "Please select a correct choice!";;
    esac
  done
  menu
}

rm -rf /root/.cache
set_paths
menu
