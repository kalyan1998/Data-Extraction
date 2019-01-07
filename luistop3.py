import json

import requests
from urllib import parse
import psycopg2
import time
classnames=set()
classnames.add('salaryslip')
classnames.add('salaryrelease')
classnames.add('salarybreakup')
classnames.add('itform')
classnames.add('form16')
classnames.add('None')
conn=psycopg2.connect("dbname=tl_backup user=sayint host=bot.sayint.ai port=5433 password=smartinsights")
cur=conn.cursor()
cur1=conn.cursor()
conn.autocommit=True
countoferrors=0
ssdic={'name':'salaryslip','true':{'positive':0,'negative':0},'false':{'positive':0,'negative':0}}
srdic={'name':'salaryrelease','true':{'positive':0,'negative':0},'false':{'positive':0,'negative':0}}
sbdic={'name':'salarybreakup' ,'true':{'positive':0,'negative':0},'false':{'positive':0,'negative':0}}
itdic={'name':'itform', 'true':{'positive':0,'negative':0},'false':{'positive':0,'negative':0}}
fdic={'name':'form16','true':{'positive':0,'negative':0},'false':{'positive':0,'negative':0}}
filenames=['form16','itform','salarybreakup','salaryrelease','salaryslip']
intents={}
scores={}
listdic=[fdic,itdic,sbdic,srdic,ssdic]
foh=open('heuristics.txt','w+')
r={}
with open('unclassified.txt','r+') as fread:
    time.sleep(0.25)
    for line in fread.readlines():
        if line=='\n':
            continue
        msgid=line.split(' ',1)[0]
        if line==' ' or line=='\t' or line=='\n' or line=='\r':
            continue
        if len(line.split(' '))<2:
            continue
        linebefore=line.split(' ',1)[1]
        line=linebefore
        msgid=msgid.replace('(','').replace(')','').replace(',','').replace('\'','')
        print(msgid,line)
        line = parse.quote(line)
        params = {
            # Query parameter
            'q': '{0}'.format(line.encode('utf-8')),
            'model':'umodel'
            # Optional request parameters, set to default values
            #'subscription-Key':'7a59937e80dd423fa5415fdbd8289275',
        }
        """r = requests.get(
            'https://westus.api.cognitive.microsoft.com/luis/webapi/v2.0/apps/087f2913-a411-4527-a031-c68948495d1d/versions/0.1/predict',
                params=params).json()"""
        #r=requests.get('https://westus.api.cognitive.microsoft.com/luis/webapi/v2.0/apps/087f2913-a411-4527-a031-c68948495d1d/versions/0.1/predict?subscription-Key=7a59937e80dd423fa5415fdbd8289275&example={0}&patternDetails=true'.format(line))
        try:
            #r=requests.get('http://172.16.6.101:5000/parse?model=umodel&q={0}'.format(line),params=None)
            r=requests.get('https://westus.api.cognitive.microsoft.com/luis/webapi/v2.0/apps/087f2913-a411-4527-a031-c68948495d1d/versions/0.1/predict?subscription-Key=7a59937e80dd423fa5415fdbd8289275&example={0}&patternDetails=true'.format(line))
            r = r.json()
            scores[msgid]={}
            scores[msgid]['message']=linebefore
            scores[msgid]['top']=r["intentPredictions"][0]["name"]
            for j,i in enumerate(r['intentPredictions']):
                if(j>2):
                    break
                scores[msgid][i['name']]=i['score']
        except Exception as e:
            countoferrors=countoferrors+1
            print(line)
            print(e.__class__)
            print('Exception caught ')
            continue
print(scores)
with open('dataunclassifiedluis.txt', 'w+') as tdfp:
    tdfp.write(json.dumps(scores))
print('errors count '+str(countoferrors))
for keyid,keyvalue in scores.items():
    """rasa original class below"""
    """cur1.execute('select a.multi_class,a.classes_tsv from emails.analytics a,emails.tracker t where a.msg_id=t.msg_id and t.msg_id=\'{0}\''.format(keyid))
    result=cur1.fetchall()
    aresult="".join(i.replace('\'','')+' ' for i in result[0][1].split(' '))
    """
    stringtop=''
    for i,j in keyvalue.items():
        if i in classnames:
            stringtop=stringtop+i+'='+str(j)+' '
    message=keyvalue['message'].replace('\'','\'\'')
    cur.execute('insert into rasa_unclassified_summary values(\'{0}\',\'{1}\',{2},\'{3}\',\'{4}\',\'{5}\')'.format(keyid,message,False,'None',keyvalue['top'],stringtop))
