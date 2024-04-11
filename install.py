#!/bin/python

import os
import sys
import subprocess

MOONRAKER_DIR = os.path.dirname(os.path.abspath(__file__))

MOONRAKER_ENV_DIR = os.path.join(MOONRAKER_DIR, "moonraker-venv")
MOONRAKER_ENV_PYTHON = os.path.join(MOONRAKER_ENV_DIR, "bin", "python")

MOONRAKER_CONFIG_DIR = os.path.join(MOONRAKER_DIR, "config")
MOONRAKER_SERVICE_DIR = os.path.join(MOONRAKER_DIR, "service")

SYSTEM_CONFIG_DIR = "/usr/data/printer_data/config"
SYSTEM_SERVICE_DIR = "/etc/init.d"

CONFIG_FILE = "moonraker.conf"
SERVICE_FILE = "S56moonraker_service"
SERVICE_TEMPLATE_FILE = "service_template"


def generate_moonraker_service():
    template_file = os.path.join(MOONRAKER_SERVICE_DIR, SERVICE_TEMPLATE_FILE)
    output_file = os.path.join(MOONRAKER_SERVICE_DIR, SERVICE_FILE)

    with open(template_file, 'r') as file:
        template = file.read()

    # Define the values to substitute in the template
    values = {
        "moonraker_env": MOONRAKER_ENV_PYTHON,
        "moonraker_dir": MOONRAKER_DIR
    }

    # Apply string formatting to substitute the values in the template
    content = template.format(**values)

    # Write the output to a new file
    with open(output_file, 'w') as file:
        file.write(content)

    print("Output file generated successfully.")

    os.chmod(output_file, 0o755)  # 0o755 corresponds to -rwxr-xr-x permissions

    print("File permissions changed successfully.")


def delete_file(file_path):
    if not os.path.exists(file_path):
        print("File does not exist.")
        return

    os.remove(file_path)

    print("File deleted successfully.")


def create_symbolic_link(source_file, symlink_file):
    if os.path.exists(symlink_file):
        os.unlink(symlink_file)
        delete_file(symlink_file)

    os.symlink(source_file, symlink_file)

    print("Symbolic link created successfully.")


def remove_symbolic_link(symlink_file):
    if not os.path.exists(symlink_file):
        return

    os.unlink(symlink_file)
    delete_file(symlink_file)

    print("Symbolic link removed successfully.")


def start_service():
    system_service_file = os.path.join(SYSTEM_SERVICE_DIR, SERVICE_FILE)

    if not os.path.exists(system_service_file):
        print("Service file does not exist.")
        return

    subprocess.call(f"{system_service_file} start", shell=True)

    print("Service started successfully.")


def stop_service():
    system_service_file = os.path.join(SYSTEM_SERVICE_DIR, SERVICE_FILE)

    if not os.path.exists(system_service_file):
        print("Service file does not exist.")
        return

    subprocess.call(f"{system_service_file} stop", shell=True)

    print("Service stopped successfully.")


def install():
    generate_moonraker_service()

    moonraker_config_file = os.path.join(MOONRAKER_CONFIG_DIR, CONFIG_FILE)
    system_config_file = os.path.join(SYSTEM_CONFIG_DIR, CONFIG_FILE)

    create_symbolic_link(moonraker_config_file, system_config_file)

    moonraker_service_file = os.path.join(MOONRAKER_SERVICE_DIR, SERVICE_FILE)
    system_service_file = os.path.join(SYSTEM_SERVICE_DIR, SERVICE_FILE)

    create_symbolic_link(moonraker_service_file, system_service_file)

    start_service()


def uninstall():
    stop_service()

    system_service_file = os.path.join(SYSTEM_SERVICE_DIR, SERVICE_FILE)
    remove_symbolic_link(system_service_file)

    system_config_file = os.path.join(SYSTEM_CONFIG_DIR, CONFIG_FILE)
    remove_symbolic_link(system_config_file)


def main():
    if len(sys.argv) < 2:
        command = "install"
    else:
        command = sys.argv[1]

    if command == "install":
        return install()

    if command == "uninstall":
        return uninstall()

    print("Invalid command. Please use 'install' or 'uninstall'")


if __name__ == '__main__':
    main()
