#
#   Copyright © 2023, SnowCoder404
#
from Crypto.PublicKey import RSA


def genarate():
    key = RSA.generate(4096)
    key_data = open('secret_key.pem', 'wb')
    key_data.write(key.export_key("PEM"))
    key_data.close()
    key_data = open('secret_key.pem','r')
    key = RSA.import_key(key_data.read()) 

key = genarate()
