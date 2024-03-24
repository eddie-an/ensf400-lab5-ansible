import ansible_runner
import urllib.request

def get_ssh_key():
    with open("./secrets/id_rsa", "r") as f:
        return f.read()

def run_ansible_playbook():
    ssh_key = get_ssh_key()
    r = ansible_runner.run(
        private_data_dir=".",
        inventory='./hosts.yml',
        playbook='./hello.yml',
        ssh_key=ssh_key
    )
    return r

def fetch_data_from_url():
    for i in range(6):
        response = urllib.request.urlopen("http://0.0.0.0")
        message = response.read().decode("utf-8")
        print(message)

if __name__ == "__main__":
    run_ansible_playbook()
    fetch_data_from_url()
