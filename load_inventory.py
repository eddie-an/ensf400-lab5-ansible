import ansible_runner
import re

# Run ansible-playbook to gather inventory and find IP addresses
response, error, code = ansible_runner.interface.run_command("ansible-playbook", [
        "-i", "./hosts.yml",
        "--private-key", "./secrets/id_rsa", 
        "./find_ip.yml"
    ],
    quiet=True
)

if code != 0:
    print("Error running the playbook")
    print(error)
    exit(1)

# Extract IP addresses using regex
ip_regex = r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
ip_addresses = re.findall(ip_regex, response)

# Get inventory details
inventory_response, error = ansible_runner.interface.get_inventory(
    action='list',
    inventories=['./hosts.yml'],
    response_format='json',
    quiet=True
)

if error:
    print("Error getting inventory details")
    print(error)
    exit(1)

# Print the name, IP addresses, and group names for all hosts
for i, host in enumerate(inventory_response["_meta"]["hostvars"]):
    print(f"Host: {host}")
    print(f"IP: {ip_addresses[i]}")
    print(f"Group: {'loadbalancer' if host == 'localhost' else 'app_group'}")
    print()

# Pinging all hosts
response, error, code = ansible_runner.interface.run_command("ansible", [
    "-i", "./hosts.yml",
    "--private-key", "./secrets/id_rsa",
    "all:localhost",
    "-m", "ping"
])

if code != 0:
    print("Error running the ping test")
    print(error)
    exit(1)
