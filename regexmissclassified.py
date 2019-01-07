import psycopg2
conn=psycopg2.connect("dbname=tl_backup user=sayint host=bot.sayint.ai port=5433 password=smartinsights")
cur=conn.cursor()
b=open('messageid.txt','w')
c=0
with open('regexsrmissclassified.txt','r') as a:
    for i in a.readlines():
        if(i==' ' or i=='\n' or i=='\t' or i=='\r'):
            continue
        i=i.strip()
        i=i.replace(" ","_").replace('\n','_').replace('\t','_').replace('\'','\'\'').replace('\\xa0','_').replace('\\t','_')
        i='\'%'+i+'%\''
        print(i)
        cur.execute('select a.msg_id from emails.analytics a,emails.tracker t where a.msg_id=t.msg_id and t.message like {0}'.format(i))
        row=cur.fetchall()
        print(row)
        if len(row)>1:
            c=c+1
            continue
        if(len(row)==0):
            continue
        b.write(str(row[0])+" "+str(i[2:-2])+'\n')
print(c)
"""import re
b=open('regexsrmissclassified.txt','w+')
with open('ssakku','r') as a:
    count=1
    for i in a.readlines():
        if re.search('salary slip',i) or re.search('Salary Slip',i):
            b.write(str(count)+" "+i)
            'chat','alpha','172.16.6.101','alpha123'
        count=count+1"""



