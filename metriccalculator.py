import json
import time
import httplib2
from idna import unicode
import requests
headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': '3f88533f3ac04af787adaeb946f26956',
}
ssdic={'name':'salaryslip','true':{'positive':0,'negative':0},'false':{'positive':0,'negative':0}}
srdic={'name':'salaryrelease','true':{'positive':0,'negative':0},'false':{'positive':0,'negative':0}}
sbdic={'name':'salarybreakup' ,'true':{'positive':0,'negative':0},'false':{'positive':0,'negative':0}}
itdic={'name':'itform', 'true':{'positive':0,'negative':0},'false':{'positive':0,'negative':0}}
fdic={'name':'form16','true':{'positive':0,'negative':0},'false':{'positive':0,'negative':0}}
filenames=['salaryslip','salaryrelease','salarybreakup','itform','form16']
listdic=[ssdic,srdic,sbdic,itdic,fdic]
for l in filenames:
    with open(l,'r+') as fread:
        for line in fread.readlines():
            params = {
                # Query parameter
                'q': '{0}'.format(line.encode("utf-8")),
                # Optional request parameters, set to default values
                'project': 'default',
                'model': 'teamleasemodel',
            }
            r = requests.get(
                'http://172.16.6.101:5000/parse',
                headers=headers, params=params)
            #print(r.json()['topScoringIntent']['intents'])
            """print(l)
            print(r.json()['topScoringIntent']['intent'])
            print(type(r.json()['topScoringIntent']['intent']))"""
            if l==r.json()['topScoringIntent']['intent']:
                for dic in listdic:
                    if dic['name']==l:
                        dic['true']['positive']+=1
                    else:
                        dic['true']['negative']+= 1
            else:
                for dic in listdic:
                    if dic['name']==l:
                        dic['false']['negative'] += 1
                    else:
                        dic['false']['positive'] += 1
a=[]
b=[]
e=[]
g=[]
#print(r.json())
for dic in listdic:
   a.append(dic['true']['positive']/(dic['false']['positive']+dic['true']['positive']))
'''for dic in listdic:
   d.append(dic['true']['positive']/(dic['true']['positive']+dic['false']['negative']))
'''
for dic in listdic:
   g.append(((dic['true']['positive']+dic['true']['negative'])/(dic['true']['positive']+dic['true']['negative']+dic['false']['positive']+dic['false']['negative'])))
for dic in listdic:
   b.append(dic['true']['positive']/(dic['true']['positive']+dic['false']['negative']))
for (c,d) in zip(a,b):
    if c==0 and d==0:
        pass
    else:
        e.append((2*c*d)/(c+d))
print(a)
print(b)
print(e)
print(g)

            #conn = httplib2.HTTPSConnectionWithTimeout("westus.api.cognitive.microsoft.com")
            #line=unicode(line,"utf-8")
            #conn.request("GET", "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/573a1ae6-4fbb-40ad-b353-6a085112755c?subscription-key=3f88533f3ac04af787adaeb946f26956&spellCheck=true&bing-spell-check-subscription-key=YOUR_BING_KEY_HERE&verbose=true&timezoneOffset=-360&q={0}".format(line.encode("utf-8