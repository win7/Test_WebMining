import pysftp
# credentials of targeted sftp server
host = "200.48.202.52"
username = "rabarca"
password = "Undqt-111"
port = 1122

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None
# And authenticate with a private key
with pysftp.Connection(host=host, 
                        username=username, 
                        password=password,
                        port=port,
                        private_key=".ppk",
                        cnopts=cnopts) as sftp:
    print("Connection succesfully stablished... ")

    # Switch to a remote directory
    sftp.cwd("in")

    # Copy file, to the current working directory on the server, preserving modification time
    sftp.put("texto.txt", preserve_mtime=False)
    print("Close connection... ")