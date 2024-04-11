#!/bin/python3

import os
import sys

MOONRAKER_DIR = os.path.dirname(os.path.abspath(__file__))

def generate_moonraker_service():
    template_file = os.path.join(MOONRAKER_DIR, "service", "S56moonraker_service_template")
    output_file = os.path.join(MOONRAKER_DIR, "service", "S56moonraker_service")

    with open(template_file, 'r') as file:
        template = file.read()

    # Define the values to substitute in the template
    values = {
        "moonraker_env": os.path.join(MOONRAKER_DIR, "moonraker-venv", "bin", "python"),
        "moonraker_dir": MOONRAKER_DIR
    }

    # Apply string formatting to substitute the values in the template
    content = template.format(**values)

    # Write the output to a new file
    with open(output_file, 'w') as file:
        file.write(content)

    print("Output file generated successfully.")

def create_symbolic_link(source_file, symlink_file):
    # Create a symbolic link
    os.symlink(source_file, symlink_file)
    print("Symbolic link created successfully.")

def remove_symbolic_link(symlink_file):
    # Remove the symbolic link
    os.unlink(symlink_file)
    print("Symbolic link removed successfully.")

def install():
    generate_moonraker_service()

    config_file = os.path.join(MOONRAKER_DIR, "config", "moonraker.conf")
    service_file = os.path.join(MOONRAKER_DIR, "service", "S56moonraker_service")

    create_symbolic_link(config_file, "/usr/data/printer_data/config/moonraker.conf")
    create_symbolic_link(service_file, "/etc/init.d/S56moonraker_service")

def uninstall():
    remove_symbolic_link("/usr/data/printer_data/config/moonraker.conf")
    remove_symbolic_link("/etc/init.d/S56moonraker_service")

def main():
    command = sys.argv[1]

    if command == "uninstall":
        return uninstall()

    return install()

if __name__ == '__main__':
    main()
