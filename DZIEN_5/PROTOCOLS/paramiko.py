import paramiko


HOST = "test.rebex.net"
USERNAME = "demo"
PASSWORD = "password"


def run_command():

    client = paramiko.SSHClient()

    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(
        hostname=HOST,
        username=USERNAME,
        password=PASSWORD
    )

    stdin, stdout, stderr = client.exec_command("ls")

    output = stdout.read().decode()

    print(output)

    with open("result.txt", "w") as f:
        f.write(output)

    client.close()


if __name__ == "__main__":
    run_command()
