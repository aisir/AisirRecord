# 分析两篇文章是否相同

def similar_check(words1, words2):
    w1 = set(words1.split(','))
    w2 = set(words2.split(','))
    if len(w1 & w2) > 15:
        return True
    else:
        return False
