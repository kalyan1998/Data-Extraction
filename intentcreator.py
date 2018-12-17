import httplib2
import json
intent=input("enter new intent to be created")
headers = {"Ocp-Apim-Subscription-Key": '3f88533f3ac04af787adaeb946f26956', "Content-Type": "application/json"}
appid='73dc6ed9-6092-4203-99bb-61789ef88fea'
conn = httplib2.HTTPSConnectionWithTimeout("api.projectoxford.ai")
conn.request("POST", "/luis/v2.0/apps/{0}/versions/0.1/intents".format(appid),
             json.dumps({"Name": intent}), headers)
response = conn.getresponse()
print(response.status)