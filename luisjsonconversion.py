import json
from pprint import pprint
data=[]
filenames=['form16','ss','sb','itform','sr']
form16f=open('form16','w+')
ssf=open('ss','w+')
sbf=open('sb','w+')
srf=open('sr','w+')
nf=open('none','w+')
itformf=open('itform','w+')
dicfiles={'salaryrelease':srf,'None':nf,'salarybreakup':sbf,'salaryslip':ssf,'form16':form16f,'itform':itformf}
with open("Teamlease.json",'r') as f:
    data=json.load(f)
for i in data['utterances']:
    dicfiles[i['intent']].write(i['text'])
    dicfiles[i['intent']].write('\n')
ssf.close()
sbf.close()
srf.close()
itformf.close()
form16f.close()