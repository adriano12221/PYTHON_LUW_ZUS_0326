import paramiko

host = "test.rebex.net"
port = 22
username = "demo"
password = "password"

transport = paramiko.Transport((host, port))
transport.connect(username=username, password=password)

sftp = paramiko.SFTPClient.from_transport(transport)

print("Lista plików:")

for file in sftp.listdir("."):
    print(file)

sftp.close()
transport.close()
