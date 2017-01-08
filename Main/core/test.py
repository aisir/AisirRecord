import jieba
from AisirRecord.settings import STOPWORD_PATH



def word_cut():
    stopword = set()
    with open(STOPWORD_PATH, 'r') as f:
        for line in f.readlines():

            stopword.add(line.strip('\n\r'))

    return stopword


a=word_cut()
print(a)