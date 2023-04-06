## 讀取官方 json 檔
import json

# Reading data back
with open("FGC_release_A.json", "r", encoding="utf-8") as f:
    data_list = json.load(f)

# Reading data back
with open("FGC_release_A_answers.json", "r", encoding="utf-8") as f:
    data_answers_list = json.load(f)



## 取出小資料 (兩筆)
#d_list = data_list[0:2]
d_list = data_list
gg=len(d_list)
J = 0
d_ans_list = []
for i in range( gg ):
    for j in range( len(d_list[i]['QUESTIONS']) ):     # 計算 d_list 每橫排的 "QUESTIONS" 數量
        d_ans_list.extend([ data_answers_list[J+j] ])    # 重複擴充 list 化的 data_answers_list[j]

    J = J + (j+1)



## 重組為 SQuAD 格式
py = -1   # python 的 index 1 為 0

answers = []
beg = 1
i = 0
j = 0

J = 0
DATA = []
for i in range( len(d_list) ):

    PARAGRAPHS = []    # SQuAD之 'paragraphs'
    QAS = []    # SQuAD之 'qas'

    for j in range( len(d_list[i]["QUESTIONS"]) ):    # 計算 d_list 每橫排的 "QUESTIONS" 數量

        # 建立SQuAD之 'answers': [{'answer_start', 'text'}, ...]
        ANSWERS = []    # SQuAD之 'answers'
        for k in range(3):

            TEXT = d_ans_list[J+j]['ANSWER']    # SQuAD之 'text'

            if TEXT != '':
                sp = d_list[i]['DTEXT'].split(TEXT)    # 用答案將文本切段
                #if len(sp) == 1:    # <尚需修正 文本無直接答案 之情況>

                if len(sp) == 2:    # 文本有1個直接答案
                    ANSWER_START = len(sp[0])    # SQuAD之 'answer_start'
                elif len(sp) == 3:
                    if k == 0:
                        ANSWER_START = len(sp[0])
                    elif k == 1:
                        ANSWER_START = len(sp[0]) + len(TEXT) + len(sp[1])
                elif len(sp) == 4:
                    if k == 0:
                        ANSWER_START = len(sp[0])
                    elif k == 1:
                        ANSWER_START = len(sp[0]) + len(TEXT) + len(sp[1])
                    elif k == 2:
                        ANSWER_START = len(sp[0]) + len(TEXT) + len(sp[1]) + len(TEXT) + len(sp[2])
            elif TEXT == '':    # 申論題 (是否題、數字題)
                ANSWER_START = []


            ANSWERS.extend([{  'answer_start':ANSWER_START,'text':TEXT }])

        # 建立SQuAD之 'qas': [{'answers', 'question', 'id'}, ...]
        QA = []

        QUESTION = d_list[i]["QUESTIONS"][j]['QTEXT']    # SQuAD之 'question'
        ID = d_list[i]["QUESTIONS"][j]['QID']    # SQuAD之 'id'

        QA.extend([{ 'answers':ANSWERS, 'question':QUESTION, 'id':ID }])
        QAS.extend(QA)

    J = J + (j - py)    # 累加 index
    print(i,j, len(d_list[i]["QUESTIONS"]))
    print(len(sp))


    # 建立SQuAD之 'paragraphs': [{'context','qas'}, ...]

    CONTEXT = d_list[i]['DTEXT']

    PARAGRAPHS.extend([{ 'context':CONTEXT, 'qas':QAS }])


    # 建立SQuAD之 'data': [{'title', 'paragraphs'}, ...]

    TITLE = d_list[i]['DID']
    DATA.extend([{ 'title':TITLE, 'paragraphs':PARAGRAPHS }])

data = { 'data':DATA }

#print(data)

ret = json.dumps(data,ensure_ascii=False)

with open('sample_SQuAD_v2.json', 'w') as outfile:
    outfile.write(ret)



