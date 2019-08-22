# coding:utf-8

from janome.tokenizer import Tokenizer
from collections import defaultdict
from tqdm import tqdm
import dill
import random
import os

def main():
    if os.path.exists('mcmcDict.pickle'):
        with open("mcmcDict.pickle", "rb") as f:
            mcmcDict = dill.load(f)
    else:
        file = open('source.txt', 'r')  # 読み込みモードでオープン
        data = file.readlines()  # readlinesでリストとして読み込む
        t = Tokenizer()
        tokenizedData = [[]]
        for text in tqdm(data):
            if text != '\n':
                tokenizedData.append([])
                for token in t.tokenize(text, wakati=True):
                    tokenizedData[-1].append(token)
        
        mcmcDict = defaultdict(lambda: defaultdict(list))
        for text in tqdm(tokenizedData):
            for idx in range(len(text)):
                if len(text)-1 == idx:
                    pass
                elif len(text)-2 == idx:
                    mcmcDict[text[idx]][text[idx + 1]].append('__END__')
                else:
                    if idx == 0:
                        mcmcDict['__FIRST__'][text[idx]].append(text[idx + 1])
                    mcmcDict[text[idx]][text[idx + 1]].append(text[idx + 2])
        with open("mcmcDict.pickle", "wb") as f:
            dill.dump(mcmcDict, f)
    
    nextList = list(mcmcDict['__FIRST__'].keys())
    generated = [
        '__FIRST__',
        nextList[random.randrange(0,len(nextList))]
        ]
    while generated[-1] != '__END__':
        print(generated[-1],end="")
        nextList = mcmcDict[generated[-2]][generated[-1]]
        generated.append(nextList[random.randrange(0,len(nextList))])

if __name__ == '__main__':
    main()
