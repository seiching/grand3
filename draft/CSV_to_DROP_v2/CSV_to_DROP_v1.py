# DROP 架構
# {'nfl_': [{'passage', 'qa_pairs'}, {p,q_p}, ...]}
#                       'qa_pairs': [{'question','answer','query_id'}, {q,a,q_i}, ...]
#                                                'answer': [{'number','unit','yesno','spans'}, {n,u,y,s}, ...]


## 讀CSV檔
import pandas as pd

FilePath = 'resultA_edit.csv'
df = pd.read_csv(FilePath, encoding='utf-8')    # 資料型態為 DataFrame

isNan = df.isnull()    # 判斷空格值 Nan


## 每橫排取出對應資料，組合成 DROP 格式
NFL = []
NFL_nLIST = []
NFL_LIST = []

DATA = {}

ANSWER = []
QA_PAIRS = []

PID = 0    # 預設文本 P 之ID
QID = 0    # 預設問題 Q 之ID
P = df['passage'][0]

for i in range( len(df) ):

    if P == df['passage'][i] or isNan['passage'][i] == True:    # '文章'若相同 or 留空
        PASSAGE = P
        ANSWER = []

    elif P != df['passage'][i]:    # '文章'若不同

        NFL_n = 'nlf_' + str(PID).zfill(4)    # DROP之 'nfl_'  <設定編號>
        NFL_nLIST.extend([NFL_n])

        # 建立DROP之 'nfl_': [{'passage', 'qa_pairs'}, {p,q_p}, ...]
        NFL.extend([{ 'passage':PASSAGE, 'qa_pairs':QA_PAIRS }])
        NFL_LIST.extend(NFL)
        
        NFL = []
        PID = PID +1    # 累加文本 P 之ID

        ANSWER = []
        QA_PAIRS = []

        PASSAGE = df['passage'][i]
        P = PASSAGE


    # 每橫排取出對應資料
    PASSAGE = P
    QUESTION = df['question'][i]
    NUMBER = df['number'][i]
    UNIT = df['unit'][i]
    YESNO = df['yesno'][i]
    SPANS = df['spans'][i]
    QUERY_ID = df['query_id'][i]

    # 若為空格值 Nan，將對應資料改為預設值
    if isNan['number'][i] == True:
        NUMBER = []
    if isNan['unit'][i] == True:
        UNIT = []
    if isNan['yesno'][i] == True:
        YESNO = ''
    if isNan['spans'][i] == True:
        SPANS = []

        
    # 建立DROP之 'answer': [{'number','unit','yesno','spans'}]
    ANSWER.extend([{ 'number':NUMBER, 'unit':UNIT, 'yesno':YESNO, 'spans':SPANS }])

    # 建立DROP之 'qa_pairs': [{'question','answer','query_id'}, {q,a,q_i}, ...]
    QA_PAIRS.extend([{ 'question':QUESTION, 'answer':ANSWER ,'query_id':QUERY_ID }])

# 最後一個文本，建立DROP之 'nfl_': [{'passage', 'qa_pairs'}, {p,q_p}, ...]
NFL.extend([{ 'passage':PASSAGE, 'qa_pairs':QA_PAIRS }])
NFL_LIST.extend(NFL)

NFL_n = 'nlf_' + str(PID).zfill(4)    # DROP之 'nfl_'  <設定編號>
NFL_nLIST.extend([NFL_n])

DATA = dict(zip( NFL_nLIST,NFL_LIST ))


## 存檔
import json

jsdumps = json.dumps(DATA, ensure_ascii=False)
fileName = 'CSV_DROP_v1.json'
outfile = open(fileName, 'w', encoding='utf-8')
outfile.write(jsdumps)
outfile.close()

