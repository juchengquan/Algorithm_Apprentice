import re
import numpy as np


file = open("test.txt", mode="r")
content = file.read()

word_list = re.sub(r"[^\w]", " ", content).lower().split()


word_tuple = []

### map
for word in word_list:
    #print("{0}: {1}".format(word, 1))
    word_tuple.append((word, 1))
    """
    if word in word_dict.keys():
        word_dict[word] += 1
    else:
        word_dict[word] = 1

    """

### reduce
word_keys= list(set([word for word, _ in word_tuple]))

### splitting
word_count = {word:[] for word in word_keys}
for target_word in word_count:
    for word, count in word_tuple:
        if target_word == word:
            word_count[word].append(1)

### reduce:
for word, ele in word_count.items():
    word_count[word] = sum(ele)
    

"""
### reduce
len_list = [len(ele) for ele in word_dict.keys()]
length_dict = {i: 0 for i in range(1,max(len_list)+1)}

for ele in word_dict.keys():
    idx = len(ele)
    length_dict[idx] += word_dict[ele]
"""
