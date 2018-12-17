from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import intentcreator.gmailmessage as q
import base64
import email


# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'

def main():
    m=q.message()
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))
    messages=list()
    count=0
    for i in m:
        if (count<301):
            app = service.users().messages().get(userId='me', id=i,format="full").execute()['snippet']
            print(app)
            messages.append(app)
            count = count + 1


    '''msg_str = base64.urlsafe_b64decode(messages['raw'].encode('ASCII'))
    mime_msg = email.message_from_string(msg_str)'''
    for i in messages:
        print(i['snippet'])

if __name__ == '__main__':
    main()