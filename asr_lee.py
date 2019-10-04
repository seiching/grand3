# coding: utf-8



# Note Batch = 1600

import os
from os import listdir
from os.path import isfile, isdir, join
import sys
import sqlite3
import speech_recognition
#from glob import glob
import pandas as pd
import wave
#import contextlib
def genfilelist(folder):
    try:
        wavlist = []
        directory = folder+'/' 
        objects = os.listdir(directory)
        for filelist in objects:
            if filelist.find('.wav') != -1:
                wavlist.append(filelist.upper())
    except Exception as e:
        print('addpatch err'+str(e))
    wavlist.sort()
    return wavlist
batch_size = 100
print(len(sys.argv))
if(len(sys.argv))<3:
    print(" param error usage: folder range_num")
    exit()
folder = sys.argv[1]
range_num = sys.argv[2]
#folder = 'A'
#range_num = 1

#file_list

filename_list = genfilelist(folder)
#filename_list

DB_folder = folder + "DB"
range_start = (int(range_num)-1)*batch_size
range_stop = int(range_num)*batch_size-1

files = listdir(folder)

if range_start > len(files):
    print("exceed file range")
    os._exit(0)
if range_stop > len(files):
    range_stop = len(files)

print('folder_name=', folder)
print('DB_folder_name=', DB_folder)
print('range_id=%d ~ %d' %(range_start, range_stop))

if not os.path.exists(DB_folder):
    os.makedirs(DB_folder)
    
# ³s±µ¸ê®Æ®w
GoogleAsrDB = DB_folder + "/" + folder + range_num +".db"
#print('GoogleAsrDB=', GoogleAsrDB)

conn = sqlite3.connect(GoogleAsrDB)
c = conn.cursor()

# Create table

c.execute('''CREATE TABLE if not exists part (filename, sentence,PRIMARY KEY(filename))''')
c.execute('delete from part')

r = speech_recognition.Recognizer()

wav_segment = 15  # xx seconds
def split_speech_recognition(wave_file, duration):
    whole_text = ''
    for i in range(int(duration//wav_segment)+1):
        #print('----------------------------------------------------------------------')
        start_duration = i*wav_segment
        wav_period = min(duration-i*wav_segment, wav_segment) 
        print('offset: %d, duration:%d...' %(start_duration, wav_period))
        try:
        # recognition file
            with speech_recognition.AudioFile(wave_file) as source:
                audio = r.record(source, offset=int(start_duration), duration=wav_period)
                part_text = r.recognize_google(audio,language='zh-tw')
                print('part_text:', part_text)
            
            whole_text = whole_text + part_text
        except  Exception as e:
            print("Failed  recognition: "+ str(e)) 
        
    print('whole_text:', whole_text)
    partfile=wave_file[2:len(wave_file)]
    print(partfile)
    try:
        c.execute("INSERT INTO part VALUES (?,?);" , (partfile, whole_text))
    except  Exception as e:
	    print("failed to insert ")
    print("Write To DB : %s,%s"%(partfile, whole_text))
#­pºâ®É¶¡
import time
tStart  = time.asctime( time.localtime(time.time()) )



# ¿ëÃÑBpart»y­µ¡A±NÀÉ¦W»P¿ëÃÑªº¤å¦r¤@¤@¼g¤J¸ê®Æ®w¤¤
for i in range(range_start, range_stop+1, 1):
    #partfile = files[i]
    # ²£¥ÍÀÉ®×ªºµ´¹ï¸ô®|
    #fullpath = join(folder, partfile)
    fullpath = folder+'/'+filename_list[i]
    # §PÂ_ fullpath ¬OÀÉ®×ÁÙ¬O¥Ø¿ý
    if isfile(fullpath):
        try:   #¦pªG»y­µÀÉ¿ëÃÑ¦³°ÝÃD¡A»Ý­n¸õ¥X³B²z
            #with speech_recognition.AudioFile(fullpath) as source:
            #kvdbg++>
            with wave.open(fullpath,'r') as f:
                frames = f.getnframes()
                rate = f.getframerate()
                duration = frames / float(rate)
                print('======================================================================')
                print('file:%s, duration:%d seconds' %(fullpath, duration))
            
            #
            # split file and recognition
            #
            split_speech_recognition(fullpath, duration)
            
            #kvdbg<++
                
            #audio = r.record(source)
            #part_text = r.recognize_google(audio,language='zh-tw')
            #print(partfile,part_text)
            #c.execute("INSERT INTO part VALUES (?,?);" , (partfile, part_text))
            #print("¼g¤J¸ê®Æ®w")

        except :
            pass
        continue    
#­pºâ®É¶¡
tFinish = time.asctime( time.localtime(time.time()) )
print(tStart)
print(tFinish)

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
