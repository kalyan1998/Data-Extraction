from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
store = file.Storage('token.json')
creds = store.get()
service = build('gmail', 'v1', http=creds.authorize(Http()))
response = service.users().labels().list(userId='me').execute()
labels = response['labels']
for label in labels:
    print('Label id: %s - Label name: %s' % (label['id'], label['name']))
print(labels)
