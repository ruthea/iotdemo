import json
from cloudant.client import Cloudant

USERNAME = '<USERNAME>'
PASSWORD = '<PASSWORD'
db_name = 'dug'

ACCOUNT_NAME = USERNAME

client = Cloudant(USERNAME, PASSWORD, account=ACCOUNT_NAME)

# Connect to the server
client.connect()

# Perform client tasks...
session = client.session()

data = {'Message': {'Consumption': 1695357, 'ID': 11111111, 'Type': 5}, 'Time': 1474682176.0}

my_database = client[db_name]
my_document = my_database.create_document(data)

if my_document.exists():
    print 'SUCCESS!!'

# Disconnect from the server
client.disconnect()
