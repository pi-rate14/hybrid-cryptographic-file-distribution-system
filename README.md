## Encrypted File Distribution System using hybrid cryptography of Symmetric AES and Asymmetric ECC

### File distribution server where a server can distribute multiple multimedia files to multiple clients, and the files are encrypted using mixed hybrid cryptography.

### Methodology:

1. AES key is generated.
2. ECC key pair is generated.
3. AES key is encrypted using ECC
4. File is encrypted using the encrypted AES key
5. AES encrypted file is again encrypted using ECC
6. Cipher data is transferred using socket to the clients
7. Clients use the Cipher to decrypt the file using ECC and AES

### Steps to run:

- Server
  1.  Put the files to be distributed in the test files section
  2.  Run "server.py"
  3.  Enter the file name with extension when prompted.
  4.  You can enter more files one by one after the first file is distributed.
- Client(s)
  1.  After the server is running, run "client.py"
  2.  The file should begin downloading
  3.  Downloaded file appears in the root directory of the project.
  4.  Run client.py again to download any more files being distributed by the server.
