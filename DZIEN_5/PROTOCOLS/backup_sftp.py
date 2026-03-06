import os
import stat
import posixpath
import socket
import paramiko


HOST = "test.rebex.net"
PORT = 22
USERNAME = "demo"
PASSWORD = "password"

REMOTE_DIR = "/pub/example"
LOCAL_DIR = "backup"


def validate_config():
    placeholders = {
        "HOST": HOST,
        "USERNAME": USERNAME,
        "PASSWORD": PASSWORD,
    }

    invalid = []
    for name, value in placeholders.items():
        if not value or (value.startswith("<") and value.endswith(">")):
            invalid.append(name)

    if invalid:
        raise ValueError(
            "Missing real configuration values for: "
            + ", ".join(invalid)
            + ". Replace placeholder values before running the script."
        )

    try:
        socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM)
    except socket.gaierror as e:
        raise ValueError(
            f"Host '{HOST}' cannot be resolved. Check the hostname, DNS, or network connection."
        ) from e


def download_directory(sftp, remote_path, local_path):
    os.makedirs(local_path, exist_ok=True)

    for item in sftp.listdir_attr(remote_path):
        remote_item = posixpath.join(remote_path, item.filename)
        local_item = os.path.join(local_path, item.filename)

        if stat.S_ISDIR(item.st_mode):
            download_directory(sftp, remote_item, local_item)
        else:
            print("Pobieram:", remote_item)
            sftp.get(remote_item, local_item)


def main():
    validate_config()

    transport = None
    sftp = None

    try:
        transport = paramiko.Transport((HOST, PORT))
        transport.connect(username=USERNAME, password=PASSWORD)
        sftp = paramiko.SFTPClient.from_transport(transport)
        download_directory(sftp, REMOTE_DIR, LOCAL_DIR)
        print("Backup completed successfully.")
    except ValueError as e:
        print("Configuration error:", e)
    except paramiko.AuthenticationException:
        print("Authentication failed. Check username and password.")
    except paramiko.SSHException as e:
        print("SSH/SFTP error:", e)
    except OSError as e:
        print("Network or filesystem error:", e)
    finally:
        if sftp is not None:
            sftp.close()
        if transport is not None:
            transport.close()


if __name__ == "__main__":
    main()
