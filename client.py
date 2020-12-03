from ftp.client import FTPClient

client = FTPClient()
[control, data] = client.request_connection('127.0.0.1')

