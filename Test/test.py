import paramiko
# https://rajansahu713.medium.com/sftp-files-transfer-using-python-59b4cead090a
# create ssh client 

ssh_client = paramiko.SSHClient()

# remote server credentials
host = "200.48.202.52"
username = "rabarca"
password = "Undqt-111"
port = 1122

# connect
""" ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=host,port=port,username=username,password=password)

print('connection established successfully')

ssh_client.close() """

# uploading
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=host,port=port,username=username,password=password)
print('connection established successfully')

# create an SFTP client object
ftp = ssh_client.open_sftp()

#---
files = ftp.listdir()

print("Listing all the files and Directory: ",files)
#---

# download a file from the remote server
files = ftp.put("texto.txt", "/")

# close the connection
ftp.close()
ssh_client.close()