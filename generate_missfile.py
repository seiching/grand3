#encoding=utf-8
#check 合併後少的檔案
import sqlite3
import csv
import os
#輸入A,B,C 放在 語音檔上一層
part=input("please input which part,A,B,C")
directory = '%s/'  %(part)
objects = os.listdir(directory)
lobject=[]
for i in objects:
  print(i.upper())
  #print(i[0].upper())
  lobject.append(i.upper())
setdir=set(lobject)
conn = sqlite3.connect('grand.db')
cursor = conn.cursor()
sql="SELECT filename from  %spart  ;"  %(part)
#cursor.execute('select * from user where id=?', ('1',))
cursor.execute(sql)
dbvalues = list(cursor.fetchall())
ldbvalues=[]

  
for i in dbvalues:
    ldbvalues.append(i[0])
    print(i[0])
sdbvalues=set(ldbvalues)
diff=setdir-sdbvalues
missfile='missing%s.csv' %(part)
#print(diff)
with open(missfile, 'w', newline='') as csvfile:
   
    fieldnames = ['filename','sentence']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
 
    writer.writeheader()
    for i in diff:
       if i[-3:]=='wav':
          print(i)
          writer.writerow({'filename': i,'sentence':' '})

conn.close()